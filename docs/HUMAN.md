# Human Context Window

Running to-do list and handoff notes for the human side of the project. Move items to done when they're checked off or stated as done.

## Status

2026-11-08: Phone inbox is built and tested offline. It needs the Discord setup below before it can do anything real.

## Next time

Run the live checks (steps 8–12) on the laptop. After that, the next triage session runs in Claude Code from `~/Documents/todo` instead of Claude.ai.

## To do

**Live checks**

- [ ] 8. `inbox/inbox pull` on the empty channel prints "Discord inbox: empty."
- [ ] 9. Send two messages from the phone, one of them multi-line. `inbox/inbox pull` shows both, oldest first, with IDs.
- [ ] 10. `inbox/inbox ack <one id>`. That message disappears on the phone, and `pull` now shows one.
- [ ] 11. Put a wrong token in `.env`. `pull` prints the "couldn't reach the inbox" line and doesn't crash. Put the right token back.
- [ ] 12. Start `claude` in `~/Documents/todo`. The inbox output should be in the session from the start. Ask Claude what's in the inbox to confirm.

**Todo repo**

- [ ] 13. Create a **private** GitHub repo for `~/Documents/todo`, then add it as the remote and push.
- [ ] 14. Bring the current list over from Claude.ai as the first week file (e.g. `week-of-nov-9-monday.md`).

## Done

- 2026-11-08: Decided on the Discord-channel inbox design (see DECISIONS.md).
- 2026-11-08: Discord setup done: private server and `#inbox`, bot app (Public Bot off, Message Content Intent on), bot invited with View Channels / Read Message History / Manage Messages, channel ID copied, `.env` filled in, channel favorited on the phone (steps 1–6).
- 2026-11-08: Hook installed: `inbox/todo-settings.json` copied to `~/Documents/todo/.claude/settings.json` (step 7).

## Good to know

- **The inbox bot always shows as "offline" in Discord. That's correct.** Discord only shows a bot as online while it holds a live connection open, and this one never does. It wakes up at session start, reads the channel, and leaves. No VPS or background service needed; messages wait in Discord until the laptop asks.
- Running the tests: `uv run pytest` from the todo-flow folder.
- The inbox command is `todo-flow/inbox/inbox pull` or `... ack <ids>`. It works from any folder.
- `~/Documents/todo/CLAUDE.md` holds the real triage instructions now. `CLAUDE.todo.md` in this repo is the older reference copy.

## Parked ideas

- **Morning pre-sort (from 2026-11-08):** a scheduled cloud agent (Claude Code `/schedule` routine) pulls the Discord inbox each morning and drafts where each item belongs in that day's todo file before you sit down. Parked because the live triage conversation is what gets things moving, and pre-sorting might quietly replace that part. Revisit once the basic inbox pipe has been in use for a while.
