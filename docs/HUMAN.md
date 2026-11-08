# Human Context Window

Running to-do list and handoff notes for the human side of the project. Move items to done when they're checked off or stated as done.

## Status

2026-11-08: The phone inbox is fully set up: the morning timer is running and the todo repo is backed up to the VPS. All that's left is the first real use, Monday morning (2026-11-09).

## Next time

Monday AM: steps 19 and 20, which are just the first real triage session in Claude Code.

## To do

**First real use (Monday AM)**

- [ ] 19. Bring the current list over from Claude.ai as the first week file (e.g. `week-of-nov-9-monday.md`).
- [ ] 20. In a fresh `claude` session in `~/Documents/todo`, ask what's in the inbox. It should answer from `inbox.md`, with no hook involved.

## Done

- 2026-11-08: Decided on the Discord-channel inbox design (see DECISIONS.md).
- 2026-11-08: Discord setup done: private server and `#inbox`, bot app (Public Bot off, Message Content Intent on), bot invited with View Channels / Read Message History / Manage Messages, channel ID copied, `.env` filled in, channel favorited on the phone (steps 1–6).
- 2026-11-08: Hook installed: `inbox/todo-settings.json` copied to `~/Documents/todo/.claude/settings.json` (step 7). *Since removed by Claude in the redesign.*
- 2026-11-08: Live checks against real Discord passed: empty inbox, multi-line messages in order with IDs, ack deletes on the phone, bad token fails soft, and the hook delivers the inbox into a Claude Code session in `~/Documents/todo` (steps 8–12).
- 2026-11-08: Decided on the inbox.md redesign: move on pull, commit only, run on wake, AGENTS.md.
- 2026-11-08: Redesign live checks passed: two messages (one multi-line) moved into `inbox.md` and committed, `#inbox` emptied, and a second pull reports nothing new (steps 15–16).
- 2026-11-08: `inbox` is a command anywhere, via a symlink at `~/.local/bin/inbox` (undo: `rm ~/.local/bin/inbox`) (step 16a).
- 2026-11-08: Morning timer linked and enabled (`systemctl --user link` + `enable --now`). It runs at 07:00, catches up on wake or boot, and logs to `journalctl --user -u inbox-pull`. To change the time, edit `OnCalendar=` in `deploy/inbox-pull.timer`, then run `systemctl --user daemon-reload` (step 17).
- 2026-11-08: Todo repo backed up to a bare repo on the VPS as remote `vps`. `git push` by hand whenever you like; the timer only commits (step 18).

## Good to know

- **The inbox bot always shows as "offline" in Discord. That's correct.** Discord only shows a bot as online while it holds a live connection open, and this one never does. It wakes up when `inbox pull` runs, moves the messages, and leaves. No VPS or background service needed; messages wait in Discord until the laptop asks.
- `inbox pull` (after step 16a; before that, use the full path `.../todo-flow/inbox/inbox pull`) moves every waiting note into `~/Documents/todo/inbox.md`, commits that file, and then clears the notes from Discord. A note with no text (e.g. just a photo) is left in Discord.
- Once a note is in `inbox.md`, the file is the only copy. Its safety net is the todo repo's git history.
- Running the tests: `uv run pytest` from the todo-flow folder.
- `~/Documents/todo/AGENTS.md` holds the real triage instructions now; `CLAUDE.md` there just points to it. `CLAUDE.todo.md` in this repo is the older reference copy.

## Parked ideas

- **Morning pre-sort (from 2026-11-08):** a scheduled cloud agent (Claude Code `/schedule` routine) pulls the Discord inbox each morning and drafts where each item belongs in that day's todo file before you sit down. Parked because the live triage conversation is what gets things moving, and pre-sorting might quietly replace that part. Revisit once the basic inbox pipe has been in use for a while.
