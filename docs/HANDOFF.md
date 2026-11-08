# Handoff

## What this repo is, in practice

Plumbing for Acacia's todo triage. The triage itself happens in conversation, now in Claude Code from `~/Documents/todo/` (it moved from Claude.ai on 2026-11-08). The real triage instructions live in `~/Documents/todo/CLAUDE.md`. `CLAUDE.todo.md` here is the older reference copy it was built from, so don't treat it as current.

## The phone inbox (built 2026-11-08)

She texts herself through a private Discord channel. The channel itself is the inbox, so there's no intermediate file, deliberately: she doesn't use files she has to append to, and it has to feel like sending a message off into the void.

- `inbox/inbox.py` (run via the `inbox/inbox` bash wrapper) has two commands. `pull` reads every non-bot message and prints it with its ID. `ack <ids>` deletes those messages.
- It's REST only, so no process runs. The `.env` at the repo root holds `INBOX_BOT_TOKEN` and `INBOX_CHANNEL_ID`.
- The SessionStart hook in the todo repo runs `pull`. The triage Claude files the items, saves the file, then runs `ack` with exactly those IDs. Deleting is the point: she wants sticky notes, not a history. It also keeps sensitive details from sitting on Discord.
- `pull` must never fail loudly, because it runs at session start. Keep that property if you touch it.
- Tests: `uv run pytest`, 5 tests, all with mocked HTTP.

## Where things stand

As of 2026-11-08, nothing has run against real Discord yet. Acacia has to do the Discord app setup and copy `inbox/todo-settings.json` into `~/Documents/todo/.claude/settings.json` herself. Auto mode blocked Claude from writing that file, since it's a hook plus a pre-approved delete. All of it is checklisted in `docs/HUMAN.md`. If she says the live checks failed, the likeliest causes are Message Content Intent being off (messages come back blank, and `pull` prints a hint) or the bot missing Manage Messages (ack fails with HTTP 403).

## Open threads

- Pre-approving `ack` was flagged, and the plan was approved, but she never answered that specific point. It's worth a one-line check sometime.
- Parked idea: a morning pre-sort routine (in HUMAN.md). Don't build it unless she brings it up.
- No attachments in v1. Image messages show as "(no text)".
