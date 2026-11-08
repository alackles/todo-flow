# Decisions

| Date | Decision | AI contribution | Human contribution |
|---|---|---|---|
| 2026-11-08 | Phone capture goes through a private Discord channel, and the channel itself is the inbox, with no intermediate file. A pull script reads it on demand, so nothing runs 24/7. | Proposed Discord-as-storage; ruled out Telegram (only holds messages ~24h until fetched), SMS (US carrier registration overhead), ntfy (short cache). | Wanted a messaging feel, not a file to append to; ruled out a new app and the Claude mobile app; agreed to Discord. |
| 2026-11-08 | Inbox items count as handled only after they're written into the todo file. Pull is read-only, and a separate ack step runs afterward. | Proposed the split so an interrupted session can't lose items. | |
| 2026-11-08 | Inbox pull runs automatically when a todo session starts (SessionStart hook in the todo repo), not as a manual step. | Proposed both options, leaned automatic. | Chose automatic. |
| 2026-11-08 | Inbox uses its own Discord bot, separate from remindlet. | Recommended separation (different server, different permissions). | Agreed: remindlet is a shared tool, this is personal tooling. |
| 2026-11-08 | Messages are deleted from Discord once filed. The inbox works like sticky notes, not a history. This also takes care of keeping sensitive details off Discord long-term. | Raised delete vs. keep, and the privacy angle. | Chose delete. |
| 2026-11-08 | Text only for v1; no attachment handling. | | Confirmed text is enough. |
| 2026-11-08 | Triage moves from Claude.ai into Claude Code, run from `~/Documents/todo/` (a new repo). Required for the session-start hook. | Pointed out the hook can't reach Claude.ai. | Chose to move triage into Claude Code. |
| 2026-11-08 | Convention: Python project via `pyproject.toml` + uv, invoked through a bash wrapper (`inbox/inbox`). Diverges from the plan's inline-script idea so tests and script share one environment. | Chose it during build. | |
| 2026-11-08 | Convention: Discord REST API only, no gateway connection, so nothing runs between sessions. | | |
| 2026-11-08 | Convention: the hook uses absolute paths. It's a personal machine, so portability isn't worth anything here. | | |
| 2026-11-08 | Convention: `pull` fails soft. Any error prints one line and exits 0, so a session never fails to start because of the inbox. | | |
| 2026-11-08 | Convention: `ack` takes explicit message IDs, never "everything pulled", so a message sent mid-session can't be deleted unseen. | | |
| 2026-11-08 | `ack` is pre-approved in the todo repo's permissions, so filing doesn't prompt each time. | Proposed and flagged it in the plan. | Approved the plan, but never answered the flagged question directly. Open to revisit; to revert, delete the `permissions` block. |
| 2026-11-08 | The todo repo's `.claude/settings.json` ships as `inbox/todo-settings.json`, which Acacia copies in by hand. | Write was blocked by the auto-mode safety check (hook + pre-approved delete in another repo); didn't work around it. | |