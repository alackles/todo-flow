# Handoff

## What this repo is, in practice

Plumbing for Acacia's todo triage. The triage itself happens in conversation, now in Claude Code (or any LLM) from `~/Documents/todo/`. It moved there from Claude.ai on 2026-11-08. The real triage instructions are in `~/Documents/todo/AGENTS.md`; `CLAUDE.md` there just imports it. `CLAUDE.todo.md` here is the older reference copy, so don't treat it as current.

## The phone inbox (built 2026-11-08, redesigned the same day)

She texts herself through a private Discord channel. On her side, it has to feel like sending a message off into the void, never like appending to a file. A file on the laptop side is fine, because only the script writes to it.

**Current design: move on pull.** `inbox/inbox pull` (a bash wrapper running `inbox.py` under uv) does five things, in order:

1. Fetches every non-bot message in the channel.
2. Adds the ones not already there to `~/Documents/todo/inbox.md`, deduping by hidden `<!-- discord:ID -->` markers. The file is written to a temp copy and swapped in.
3. Commits only that file, as "todo-flow inbox".
4. Deletes from Discord everything that's now in the file.
5. Leaves messages with no text in Discord, so nothing gets deleted with nothing saved.

After that, any LLM reads `inbox.md`, files the entries into the week file, then removes them and commits. A systemd user timer (`deploy/`) runs the pull at 07:00 with `Persistent=true`, and retries on failure for wifi-after-wake. Nothing else triggers it.

**Superseded first design, so you know what the history is about:** the first version used a SessionStart hook that printed the inbox, plus an `ack` command that Claude ran after filing. Acacia preferred something less automatic and not tied to Claude, so `ack` and the hook are gone. Don't bring them back.

The invariant across both designs: a note must never exist nowhere. It's in Discord until it's safely in the file, and in the file until it's in the week file.

Tests: `uv run pytest` runs 4 tests with fake HTTP and a fake git. During the build, `commit_inbox` was smoke-tested once by hand against a throwaway repo.

## Where things stand

As of 2026-11-08, the redesign hasn't been run live yet. Acacia's remaining steps, listed in `docs/HUMAN.md`, are:

- a live pull
- installing the timer
- adding the VPS remote for the todo repo (a bare repo on her VPS, not GitHub)
- bringing her current list over from Claude.ai

Earlier she had wanted to work out VPS things herself by asking questions. HUMAN.md has commands for the remote, but if she asks, let her lead.

## Open threads

- Parked idea: a morning pre-sort routine (in HUMAN.md). Don't build it unless she brings it up.
- No attachments; a photo stays in Discord. If she starts sending photos, that's the next feature.
