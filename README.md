# todo-flow

Plumbing for a to-do system that's really a conversation. The list lives in plain Markdown files, and each day I talk through it with Claude, which plays executive assistant and body double. This repo holds the small tools that make that loop smoother without making it more complicated.

## Phone inbox

**The problem:** a task occurs to me while I'm away from the laptop, and I want to throw it somewhere and forget it. I don't want to open a file, and I don't want a new app.

**How it works:**

1. On my phone, I type the thought into a private Discord channel (`#inbox`), in plain language, and send it. That's the whole thing.
2. Next time I start a triage session on the laptop, a startup hook reads the channel and hands everything waiting there to Claude.
3. Claude folds those items into the to-do list as part of the normal "what's new?" step.
4. Once an item is actually written into the list file, Claude deletes its Discord message. Whatever is still in the channel hasn't been picked up yet, like sticky notes nobody has peeled off.

Nothing runs in the background. Discord holds the messages until the laptop asks for them.

## For coders

- `inbox/inbox.py` reads (`pull`) and deletes (`ack <ids>`) messages through Discord's REST API, using a bot token. `inbox/inbox` is a wrapper that runs it with uv from any directory.
- `pull` is read-only and fails soft: errors print one line and exit 0, because it runs as a Claude Code `SessionStart` hook.
- `ack` deletes only the message IDs it's given.
- `inbox/todo-settings.json` is the hook and permission config for the todo repo's `.claude/settings.json`.

Setup: create a Discord application and bot with **Message Content Intent** on, then invite it to your channel with View Channels, Read Message History, and Manage Messages. Copy `.env.example` to `.env` and fill it in, then copy the settings file into your todo repo. The full checklist is in [docs/HUMAN.md](docs/HUMAN.md).

Tests: `uv run pytest`.

## Docs

- [docs/SPEC.md](docs/SPEC.md): the original (deliberately thin) spec
- [docs/DECISIONS.md](docs/DECISIONS.md): what got decided, and by whom
- [docs/HUMAN.md](docs/HUMAN.md): setup steps and to-dos for me
- [docs/HANDOFF.md](docs/HANDOFF.md): notes for the next Claude session
- [docs/plans/](docs/plans/): approved build plans
