# Discord inbox: phone → todo triage

## Context

Acacia wants to fire off a thought from her phone (Galaxy S22) and have it turn up in her next todo triage session, without it ever feeling like appending to a file. Decisions so far (see docs/DECISIONS.md):

- A private Discord channel *is* the inbox.
- Pulling is read-only. Filing an item then deletes its message, sticky-note style.
- The pull runs automatically at session start.
- The bot is separate from remindlet.
- Text only.

New today: triage is moving from Claude.ai into Claude Code, run from `~/Documents/todo/`. That folder is empty and not yet a git repo, so this build sets it up too.

## What gets built

### 1. todo-flow: `inbox/inbox.py`
A single uv script with its dependencies declared inside it (PEP 723: `requests`, `python-dotenv`), so there's no venv to manage. It talks to Discord's REST API only, with no gateway connection and no long-running process.

- `pull`: fetches every non-bot message in the channel, paginating 100 at a time. It prints them oldest first, as `[message_id] Sat Nov 8, 9:14 PM: text`, with the lines of multi-line messages indented. A short header tells the triage Claude what these are and that they must be acked after filing. An empty inbox prints `Discord inbox: empty.` so it's clear the hook ran.
- `ack ID [ID ...]`: deletes the given messages. Each ID gets its own ok/failed line, and one failure doesn't stop the rest. It honors 429 `retry_after`. It takes explicit IDs rather than "everything pulled", so a message sent mid-session can't be deleted unseen.
- **Fails soft:** with no network, a bad token or a missing `.env`, it prints one line ("couldn't reach the inbox; messages are still safe in Discord") and exits 0. It must never block a session from starting.
- **Message Content intent check:** if messages come back with empty content, it prints a hint that the intent is off in the developer portal. That's the most likely setup mistake.
- It loads `.env` from the script's own directory, because the hook runs with the todo repo as its working directory.

Supporting files: `.env.example` (`INBOX_BOT_TOKEN`, `INBOX_CHANNEL_ID`), and `.gitignore` covering `.env`.

### 2. todo-flow: small tests (`tests/test_inbox.py`)
About 4 tests, run with `uv run --with pytest pytest`. They cover:
- output ordering and multi-line formatting
- the empty inbox
- soft failure when the HTTP call raises
- `ack` carrying on past a single failed delete

HTTP gets mocked at one seam, so the tests never hit Discord.

### 3. `~/Documents/todo/` scaffold (separate repo, its own commit)
- `git init`
- `CLAUDE.md` built from `CLAUDE.todo.md` (minus its meta note at the top), with an **Inbox** section added:
  - Session start: the hook output appears in context. Inbox items go alongside "what's new" in the opening routine.
  - Every inbox item ends the session in one of two states. Either it's written into the current file (Floating at minimum), or Acacia has dropped it.
  - Only after the file is saved does Claude run `ack` with exactly those IDs.
- `.claude/settings.json`:
  - A SessionStart hook (matcher `startup|clear`, timeout 20s) running `uv run --quiet <abs path>/todo-flow/inbox/inbox.py pull`.
  - A permission allow rule for that script's `ack` subcommand, so filing doesn't prompt each time. **Flagging this one:** it pre-approves a delete. I think that's right, since filing comes first, but say so if you'd rather approve each ack.
- `.gitignore`

### 4. Docs (todo-flow)
- **HUMAN.md To-do:** the Discord setup checklist:
  1. Create a private server and an `#inbox` channel.
  2. In the developer portal, create a new application and bot, turn Public Bot off, and turn **Message Content Intent** on.
  3. Invite the bot with the View Channel, Read Message History and Manage Messages permissions.
  4. Turn on Developer Mode, then copy the channel ID.
  5. Fill in `.env`.
  6. On the phone, pin or favorite the channel.
  7. Create a private GitHub remote for `~/Documents/todo` and push to it.
  8. Bring the current list over from Claude.ai as the first week file.
- **DECISIONS.md:** your decision that triage moves from Claude.ai into Claude Code in `~/Documents/todo/`, plus these conventions, one line each:
  - uv inline script
  - REST only, no gateway
  - absolute path in the hook
  - fail-soft hook
  - explicit-ID ack
  - pre-allowed ack (pending your answer above)
- **HANDOFF.md:** a narrative note covering the architecture, the fact that the real todo instructions now live in `~/Documents/todo/CLAUDE.md` (so `CLAUDE.todo.md` here is a reference copy), and where things stand.
- **README.md:** replace the template text with a short "what this is / how the inbox works / setup" page.
- Save this plan to `docs/plans/2026-11-08-discord-inbox.md`.

Commits: small, authored as Claude, straight to `main`, since this is a personal repo with one commit so far. Order: script + tests, then docs. The todo repo gets one initial commit.

## Verification

1. Run the tests (`uv run --with pytest pytest`); they should pass.
2. Once you've done the Discord setup: `pull` on an empty channel prints "empty".
3. Send two messages from the phone, one of them multi-line. `pull` shows both, in order, with IDs.
4. `ack` one ID. It disappears on the phone, and `pull` now shows one message.
5. Break the token in `.env`. `pull` prints the soft-fail line and exits 0.
6. Start Claude Code in `~/Documents/todo`. The inbox output appears at session start.

Steps 2–6 need your Discord setup first, so I'll run the tests and you'll run the live checks. They go in HUMAN.md.
