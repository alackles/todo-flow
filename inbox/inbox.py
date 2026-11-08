"""Read and clear the Discord inbox channel.

    inbox pull            print every waiting message (never deletes anything)
    inbox ack ID [ID ...] delete messages that have been filed into the todo list

Talks to Discord's REST API with a bot token; nothing stays running.
Reads INBOX_BOT_TOKEN and INBOX_CHANNEL_ID from the .env at the repo root,
found relative to this file so it works from any working directory.
Run it through the `inbox` wrapper next to this file.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

API = "https://discord.com/api/v10"
ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
WRAPPER = Path(__file__).resolve().parent / "inbox"
# Plain messages and replies. Skips pins, joins, and other system messages.
USER_MESSAGE_TYPES = {0, 19}

SOFT_FAIL = (
    "Discord inbox: couldn't reach the inbox ({reason}). "
    "Messages are still safe in Discord; nothing was lost."
)
BLANK_HINT = (
    "(Every message came back blank. Message Content Intent is probably off: "
    "Discord developer portal -> the inbox app -> Bot -> Message Content Intent.)"
)


class InboxError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


def load_config():
    load_dotenv(ENV_PATH)
    token = os.environ.get("INBOX_BOT_TOKEN", "").strip()
    channel = os.environ.get("INBOX_CHANNEL_ID", "").strip()
    if not token or not channel:
        raise InboxError(f"INBOX_BOT_TOKEN or INBOX_CHANNEL_ID missing from {ENV_PATH}")
    return token, channel


def request(token, method, path, params=None):
    """One Discord API call, waiting out rate limits. Errors never include the token."""
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot (todo-flow inbox, 0.1)",
    }
    for _ in range(3):
        resp = requests.request(method, API + path, headers=headers, params=params, timeout=10)
        if resp.status_code == 429:
            try:
                wait = float(resp.json().get("retry_after", 1))
            except ValueError:
                wait = 1.0
            time.sleep(min(wait, 10))
            continue
        if resp.status_code >= 400:
            raise InboxError(f"Discord said HTTP {resp.status_code}", status=resp.status_code)
        return resp
    raise InboxError("rate limited by Discord")


def fetch_messages(token, channel):
    """Every user-written message in the channel, oldest first."""
    messages, before = [], None
    while True:
        params = {"limit": 100}
        if before:
            params["before"] = before
        batch = request(token, "GET", f"/channels/{channel}/messages", params).json()
        messages.extend(batch)
        if len(batch) < 100:
            break
        before = batch[-1]["id"]  # Discord returns newest first
    kept = [
        m for m in messages
        if not m["author"].get("bot") and m.get("type", 0) in USER_MESSAGE_TYPES
    ]
    # Message IDs are snowflakes, which sort by creation time.
    return sorted(kept, key=lambda m: int(m["id"]))


def delete_message(token, channel, message_id):
    """True if deleted, False if it was already gone."""
    try:
        request(token, "DELETE", f"/channels/{channel}/messages/{message_id}")
    except InboxError as e:
        if e.status == 404:
            return False
        raise
    return True


def format_when(timestamp):
    local = datetime.fromisoformat(timestamp).astimezone()
    return local.strftime("%a %b %-d, %-I:%M %p")


def format_pull(messages):
    if not messages:
        return "Discord inbox: empty."
    lines = [
        f"Discord inbox: {len(messages)} message(s) from Acacia's phone, oldest first.",
        "File each one into the todo list (or drop it if she says so), save the file,",
        f"then delete exactly those with: {WRAPPER} ack <id> [<id> ...]",
        "Anything not acked stays in Discord and shows up again next session.",
        "",
    ]
    for m in messages:
        text = m.get("content") or "(no text)"
        first, *rest = text.splitlines() or ["(no text)"]
        lines.append(f"[{m['id']}] {format_when(m['timestamp'])}: {first}")
        lines.extend(f"    {line}" for line in rest)
    if all(not m.get("content") for m in messages):
        lines += ["", BLANK_HINT]
    return "\n".join(lines)


def cmd_pull():
    # This runs as a session-start hook, so it must never fail loudly.
    try:
        token, channel = load_config()
        print(format_pull(fetch_messages(token, channel)))
    except Exception as e:
        print(SOFT_FAIL.format(reason=e))
    return 0


def cmd_ack(ids):
    if not ids:
        print("usage: inbox ack <message id> [<message id> ...]")
        return 2
    try:
        token, channel = load_config()
    except InboxError as e:
        print(f"Discord inbox: {e}")
        return 1
    failed = 0
    for mid in ids:
        if not mid.isdigit():
            failed += 1
            print(f"[{mid}] skipped: not a message ID")
            continue
        try:
            deleted = delete_message(token, channel, mid)
            print(f"[{mid}] deleted" if deleted else f"[{mid}] already gone")
        except Exception as e:
            failed += 1
            print(f"[{mid}] FAILED, still in Discord: {e}")
    return 1 if failed else 0


def main(argv):
    if argv[:1] == ["pull"]:
        return cmd_pull()
    if argv[:1] == ["ack"]:
        return cmd_ack(argv[1:])
    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
