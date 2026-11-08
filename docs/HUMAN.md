# Human Context Window

Running to-do list and handoff notes for the human side of the project. Move items to done when they're checked off or stated as done.

## Status

2026-11-08: Inbox redesign is built: `inbox pull` now moves Discord messages into `~/Documents/todo/inbox.md` and commits it. The session-start hook has been removed. Tests pass. The live run and timer install are yours.

## Next time

Steps 15–17: one live pull, then install the morning timer. After that, the todo repo steps.

## To do

**Inbox redesign: live checks**

- [ ] 15. Send two messages from the phone, one of them multi-line. Run `inbox/inbox pull` from any folder. Check that:
  - `~/Documents/todo/inbox.md` has both entries
  - `git -C ~/Documents/todo log --oneline` shows `inbox: +2 from phone`
  - `#inbox` is empty on the phone
- [ ] 16. Run `inbox/inbox pull` again. It should print "Inbox: nothing new." and make no new commit.

**Morning timer** (from the todo-flow folder)

- [ ] 17. Install and turn on the timer:
  ```
  systemctl --user link "$PWD/deploy/inbox-pull.service" "$PWD/deploy/inbox-pull.timer"
  systemctl --user enable --now inbox-pull.timer
  systemctl --user list-timers inbox-pull.timer      # shows the next 07:00 run
  systemctl --user start inbox-pull.service          # one run now, as a test
  journalctl --user -u inbox-pull -n 20              # what that run printed
  ```
  To change the time, edit `OnCalendar=` in `deploy/inbox-pull.timer`, then run `systemctl --user daemon-reload`.

**Todo repo**

- [ ] 18. Back up `~/Documents/todo` to the VPS (instead of GitHub). Make a bare repo there, add it as a remote, and push. If you'd rather work this one out yourself, ignore the commands:
  ```
  ssh <vps> 'git init --bare ~/backups/todo.git'
  git -C ~/Documents/todo remote add vps <vps>:backups/todo.git
  git -C ~/Documents/todo push -u vps main
  ```
  After that, `git push` whenever you feel like it. The timer only commits, never pushes.
- [ ] 19. Bring the current list over from Claude.ai as the first week file (e.g. `week-of-nov-9-monday.md`).
- [ ] 20. In a fresh `claude` session in `~/Documents/todo`, ask what's in the inbox. It should answer from `inbox.md`, with no hook involved.

## Done

- 2026-11-08: Decided on the Discord-channel inbox design (see DECISIONS.md).
- 2026-11-08: Discord setup done: private server and `#inbox`, bot app (Public Bot off, Message Content Intent on), bot invited with View Channels / Read Message History / Manage Messages, channel ID copied, `.env` filled in, channel favorited on the phone (steps 1–6).
- 2026-11-08: Hook installed: `inbox/todo-settings.json` copied to `~/Documents/todo/.claude/settings.json` (step 7). *Since removed by Claude in the redesign.*
- 2026-11-08: Live checks against real Discord passed: empty inbox, multi-line messages in order with IDs, ack deletes on the phone, bad token fails soft, and the hook delivers the inbox into a Claude Code session in `~/Documents/todo` (steps 8–12).
- 2026-11-08: Decided on the inbox.md redesign: move on pull, commit only, run on wake, AGENTS.md.

## Good to know

- **The inbox bot always shows as "offline" in Discord. That's correct.** Discord only shows a bot as online while it holds a live connection open, and this one never does. It wakes up when `inbox pull` runs, moves the messages, and leaves. No VPS or background service needed; messages wait in Discord until the laptop asks.
- `inbox/inbox pull` works from any folder. It moves every waiting note into `~/Documents/todo/inbox.md`, commits that file, and then clears the notes from Discord. A note with no text (e.g. just a photo) is left in Discord.
- Once a note is in `inbox.md`, the file is the only copy. Its safety net is the todo repo's git history.
- Running the tests: `uv run pytest` from the todo-flow folder.
- `~/Documents/todo/AGENTS.md` holds the real triage instructions now; `CLAUDE.md` there just points to it. `CLAUDE.todo.md` in this repo is the older reference copy.

## Parked ideas

- **Morning pre-sort (from 2026-11-08):** a scheduled cloud agent (Claude Code `/schedule` routine) pulls the Discord inbox each morning and drafts where each item belongs in that day's todo file before you sit down. Parked because the live triage conversation is what gets things moving, and pre-sorting might quietly replace that part. Revisit once the basic inbox pipe has been in use for a while.
