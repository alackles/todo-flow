"""Move phone notes from the Discord inbox channel into inbox.md.

    inbox pull    add every waiting message to inbox.md, commit it, then
                  delete those messages from Discord

Talks to Discord's REST API with a bot token; nothing stays running.
Reads INBOX_BOT_TOKEN, INBOX_CHANNEL_ID and (optionally) INBOX_FILE from the
.env at the repo root, found relative to this file so it works from any
working directory. Run it through the `inbox` wrapper next to this file.
"""

import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

API = "https://discord.com/api/v10"
ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
DEFAULT_INBOX = "~/Documents/todo/inbox.md"
# Plain messages and replies. Skips pins, joins, and other system messages.
USER_MESSAGE_TYPES = {0, 19}
# Hidden marker on each entry, so a message is never added twice.
ID_MARKER = re.compile(r"<!-- discord:(\d+) -->")

HEADER = """# Inbox

Notes sent from Acacia's phone, oldest first, moved here by `inbox pull`.
Remove an entry only after it's filed in the week file (see AGENTS.md).
"""
NO_TEXT_NOTE = (
    "{n} message(s) had no text and were left in Discord. Attachments aren't "
    "supported. If every message looks blank, Message Content Intent is off: "
    "Discord developer portal -> the inbox app -> Bot -> Message Content Intent."
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
    inbox = Path(os.environ.get("INBOX_FILE", "").strip() or DEFAULT_INBOX).expanduser()
    return token, channel, inbox


def request(token, method, path, params=None):
    """One Discord API call, waiting out rate limits. Errors never include the token."""
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "DiscordBot (todo-flow inbox, 0.2)",
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


def format_entry(m):
    first, *rest = m["content"].splitlines()
    lines = [f"- {format_when(m['timestamp'])}: {first} <!-- discord:{m['id']} -->"]
    lines += [f"  {line}".rstrip() for line in rest]
    return "\n".join(lines)


def existing_ids(path):
    return set(ID_MARKER.findall(path.read_text())) if path.exists() else set()


def add_to_inbox(path, entries):
    """Append entries to inbox.md. Written to a temp file and swapped in, so a
    crash mid-write leaves the old file intact rather than a half-written one."""
    text = path.read_text() if path.exists() else HEADER + "\n"
    if not text.endswith("\n"):
        text += "\n"
    text += "\n".join(entries) + "\n"
    mode = path.stat().st_mode if path.exists() else 0o644
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".inbox-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def commit_inbox(path, count):
    """Commit only inbox.md, so nothing else that happens to be staged rides along."""
    git = ["git", "-C", str(path.parent)]
    subprocess.run(git + ["add", "--", path.name], check=True, capture_output=True)
    subprocess.run(
        git + ["commit", "--quiet", "--author", "todo-flow inbox <inbox@localhost>",
               "-m", f"inbox: +{count} from phone", "--", path.name],
        check=True, capture_output=True,
    )


def cmd_pull():
    try:
        token, channel, inbox = load_config()
        messages = fetch_messages(token, channel)
    except Exception as e:
        print(f"Discord inbox: couldn't reach it ({e}). Nothing was moved.", file=sys.stderr)
        return 1

    # A message with no text can't be written down, so it stays in Discord.
    textless = [m for m in messages if not m.get("content", "").strip()]
    messages = [m for m in messages if m.get("content", "").strip()]
    if textless:
        print(NO_TEXT_NOTE.format(n=len(textless)), file=sys.stderr)

    seen = existing_ids(inbox)
    new = [m for m in messages if m["id"] not in seen]
    if new:
        try:
            add_to_inbox(inbox, [format_entry(m) for m in new])
        except OSError as e:
            print(f"Couldn't write {inbox} ({e}). Nothing was deleted from Discord.",
                  file=sys.stderr)
            return 1
        try:
            commit_inbox(inbox, len(new))
        except (OSError, subprocess.CalledProcessError) as e:
            print(f"Warning: saved to {inbox} but not committed ({e}).", file=sys.stderr)

    # Everything with text is now safely in the file, including any left over
    # from an earlier run whose delete failed, so all of it can go.
    failed = 0
    for m in messages:
        try:
            delete_message(token, channel, m["id"])
        except Exception as e:
            failed += 1
            print(f"[{m['id']}] couldn't delete from Discord ({e}). It's safe in the "
                  "file and won't be added twice.", file=sys.stderr)

    print(f"Moved {len(new)} message(s) to {inbox}." if new else "Inbox: nothing new.")
    return 1 if failed else 0


def main(argv):
    if argv[:1] == ["pull"]:
        return cmd_pull()
    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
