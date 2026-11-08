# Human Context Window

Running to-do list and handoff notes for the human side of the project. Move items to done when they're checked off or stated as done.

## Status

2026-11-08: Phone inbox is built and tested offline. It needs the Discord setup below before it can do anything real.

## Next time

Do the Discord setup (steps 1–6), then the live checks. After that, the next triage session runs in Claude Code from `~/Documents/todo` instead of Claude.ai.

## To do

**Discord setup** (one-time, about 15 minutes)

- [ ] 1. In Discord, create a new private server just for yourself, with one text channel called `#inbox`.
- [ ] 2. Go to https://discord.com/developers/applications and create a **New Application** (name it whatever, e.g. "inbox"). Then, in the **Bot** tab:
  - turn **Public Bot** off
  - turn **Message Content Intent** on (without it, every message comes back blank)
  - click **Reset Token** and copy the token
- [ ] 3. Invite the bot to your server. In the **OAuth2 → URL Generator** tab, tick the `bot` scope, then tick these permissions: **View Channels**, **Read Message History**, **Manage Messages**. Open the generated URL and pick your inbox server.
- [ ] 4. In Discord, turn on **Settings → Advanced → Developer Mode**, then right-click `#inbox` → **Copy Channel ID**.
- [ ] 5. In todo-flow, `cp .env.example .env` and paste in the token and channel ID.
- [ ] 6. On the phone, open the server and favorite the `#inbox` channel so it's one tap away.

**Hook install** (Claude was blocked from writing this file itself, which seems reasonable)

- [ ] 7. `mkdir -p ~/Documents/todo/.claude && cp inbox/todo-settings.json ~/Documents/todo/.claude/settings.json`. It holds the session-start hook and lets `ack` run without a permission prompt. If you'd rather approve each ack, delete the `permissions` block.

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

## Good to know

- Running the tests: `uv run pytest` from the todo-flow folder.
- The inbox command is `todo-flow/inbox/inbox pull` or `... ack <ids>`. It works from any folder.
- `~/Documents/todo/CLAUDE.md` holds the real triage instructions now. `CLAUDE.todo.md` in this repo is the older reference copy.

## Parked ideas

- **Morning pre-sort (from 2026-11-08):** a scheduled cloud agent (Claude Code `/schedule` routine) pulls the Discord inbox each morning and drafts where each item belongs in that day's todo file before you sit down. Parked because the live triage conversation is what gets things moving, and pre-sorting might quietly replace that part. Revisit once the basic inbox pipe has been in use for a while.
