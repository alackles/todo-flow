# todo-flow

Plumbing for a to-do system that's really a conversation. The list lives in plain Markdown files, and each day I talk through it with Claude, which plays executive assistant and body double. This repo holds the small tools that make that loop smoother without making it more complicated.

## Phone inbox

**The problem:** a task occurs to me while I'm away from the laptop, and I want to throw it somewhere and forget it. I don't want to open a file, and I don't want a new app.

**How it works:**

1. On my phone, I type the thought into a private Discord channel (`#inbox`), in plain language, and send it. That's the whole thing.
2. Each morning, a timer on the laptop moves everything waiting in the channel into `inbox.md` in my to-do folder, then clears it from Discord. I can also do this any time with `inbox pull`.
3. When I sit down to triage, whichever LLM I'm working with reads `inbox.md` and folds the notes into the to-do list as part of the normal "what's new?" step.
4. Once a note is actually written into the week's list, its line is removed from `inbox.md`. Whatever's still there hasn't been dealt with yet, like sticky notes nobody has peeled off.

Nothing runs in the background. Discord holds the messages until the laptop asks for them, and the bot shows as "offline" the whole time.

## For coders

- `inbox/inbox.py pull` reads the channel through Discord's REST API with a bot token. It appends new messages to `inbox.md` (written to a temp file and swapped in, deduped by a hidden `<!-- discord:ID -->` marker per entry), commits just that file, and only then deletes the messages from Discord. Messages with no text are left alone. `inbox/inbox` is a wrapper that runs it with uv from any directory.
- `deploy/` has a systemd user service and timer: a daily 07:00 run, catch-up after sleep or shutdown, and a retry every minute (up to 5 tries) if the network isn't up yet.
- The to-do repo's instructions live in `AGENTS.md`, so the inbox doesn't depend on any one LLM tool.

Setup: create a Discord application and bot with **Message Content Intent** on, then invite it to your channel with View Channels, Read Message History, and Manage Messages. Copy `.env.example` to `.env` and fill it in (`INBOX_FILE` sets where notes land). Then link and enable the timer. The full checklist is in [docs/HUMAN.md](docs/HUMAN.md).

Tests: `uv run pytest`.

## Docs

- [docs/SPEC.md](docs/SPEC.md): the original (deliberately thin) spec
- [docs/DECISIONS.md](docs/DECISIONS.md): what got decided, and by whom
- [docs/HUMAN.md](docs/HUMAN.md): setup steps and to-dos for me
- [docs/HANDOFF.md](docs/HANDOFF.md): notes for the next Claude session
- [docs/plans/](docs/plans/): approved build plans
