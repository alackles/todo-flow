# Inbox redesign: Discord → inbox.md

## Context

The first build works end to end. Each Claude Code session starts with a hook that pulls messages from Discord, and Claude deletes each message once it's filed. Acacia wants that slightly less automated, and not tied to Claude:

- `inbox pull`, run from anywhere, moves Discord messages into a plain `inbox.md` in the todo repo.
- Any LLM reads `inbox.md` as the inbox, rather than calling the tool.
- A morning timer runs the pull, and also catches up on wake if the laptop was asleep. Nothing else triggers it.

Decisions so far (in DECISIONS.md except where noted):

- **Move on pull:** messages are deleted from Discord as soon as they're safely in the file.
- **`inbox.md` is committed:** `pull` auto-commits it. Commit only, no push; Acacia pushes manually. *Not yet logged.*
- **Todo repo backup:** its remote is a bare git repo on her VPS, not GitHub. todo-flow stays on GitHub. *Not yet logged.*
- **Catch-up on wake:** the timer runs a missed pull when the laptop wakes.
- **AGENTS.md** is the shared instruction file, and CLAUDE.md points to it.

## Changes

### 1. `inbox/inbox.py`: pull becomes "move"
- **New config:** `INBOX_FILE` in `.env`, defaulting to `~/Documents/todo/inbox.md`.
- **`pull` sequence:**
  1. Fetch messages. Reuse `fetch_messages` and `request` as they are.
  2. Read the existing `inbox.md`. Collect the IDs already in it from the hidden `<!-- discord:ID -->` markers.
  3. Format any messages not already there and add them to the file. Write to a temp file and swap it in with `os.replace`, so a crash mid-write can't corrupt the inbox. If the file doesn't exist yet, create it with a short header first.
  4. If anything was added, commit only `inbox.md`, with message `inbox: +N from phone` and author "todo-flow inbox". The commit is limited to that one file so it never sweeps up other changes you've staged. If the commit fails, print a warning and carry on: the file is already saved.
  5. Delete **every** fetched message from Discord. That includes ones already in the file whose earlier delete failed. Deletes happen only after step 3 succeeds.
  6. Print one line, e.g. `Moved 3 message(s) to ~/Documents/todo/inbox.md.` or `Inbox: nothing new.`
- **Entry format:** `- Sat Nov 8, 9:14 PM: text <!-- discord:123 -->`. Continuation lines of multi-line messages are indented two spaces. Clearing an entry means removing the bullet and its indented lines.
- **Exit codes change.** `pull` no longer runs as a hook, so it exits 1 when it can't reach Discord. That's what lets the timer's retry kick in. The blank-content hint stays, printed to stderr.
- **Removed:** `ack`, `delete`-by-CLI, the instruction block printed for Claude, and the soft-fail rule. `delete_message` stays, since pull uses it internally.
- **`inbox/inbox` wrapper:** when uv is missing it now exits 1 instead of 0.

### 2. Tests (`tests/test_inbox.py`): 5 → 4
- **Kept:** fetch is oldest first and skips bot and system messages.
- **Kept, adapted:** entry formatting (timestamp, text, ID marker, two-space indent for continuation lines).
- **New:** pull adds only messages not already in the file, and deletes all fetched messages afterward. This covers the dedupe and the leftovers from failed deletes.
- **New:** if the file write fails, nothing is deleted from Discord. This is the data-integrity test.
- **Removed:** empty-inbox output, the soft-fail test, and the ack test, since those behaviors are gone.
- The git commit sits behind one function (`commit_inbox`) that the tests replace with a fake, so tests never run git.

### 3. Morning timer: `deploy/inbox-pull.service` + `deploy/inbox-pull.timer` (systemd user units)
- **Service:**
  - `Type=oneshot`, running `.../inbox/inbox pull`.
  - `Restart=on-failure` with `RestartSec=60`, capped by `StartLimitBurst=5` within `StartLimitIntervalSec=600`. That's 5 attempts a minute apart, which covers wifi still reconnecting after wake. (systemd 255 is installed, which supports restarting oneshot services.)
- **Timer:** `OnCalendar=*-*-* 07:00` with `Persistent=true`. 07:00 is a placeholder; it's one line to change.
  - **Missed while powered off:** `Persistent=true` runs the pull at the next boot.
  - **Missed while suspended:** a calendar timer that came due during suspend fires on resume.
- **Install is a HUMAN.md step:** symlink both units into `~/.config/systemd/user/`, then `systemctl --user daemon-reload && systemctl --user enable --now inbox-pull.timer`. It's left to you because it sets up a persistent scheduled job on your machine.

### 4. Todo repo (`~/Documents/todo`)
- **New `AGENTS.md`** with the full instructions, moved from today's CLAUDE.md. The inbox section is rewritten:
  - At session start, read `inbox.md`.
  - Present its entries as part of "what's new."
  - Once the week file is saved, remove the filed (or dropped) entries from `inbox.md`.
  - Commit both files together.
  - If she says she just sent something, run `inbox pull` or ask her to.
- **`CLAUDE.md`** shrinks to an `@AGENTS.md` import plus one line explaining why.
- **`inbox.md`** is seeded with the header only, so AGENTS.md doesn't point at a missing file.
- **`.claude/settings.json`** (the old hook plus the ack permission) is now obsolete. It's untracked, and you installed it. I'll read it first, then try to remove it. If that's blocked, it becomes a HUMAN.md step.
- One commit, authored as Claude.

### 5. todo-flow docs and cleanup
- **Delete** `inbox/todo-settings.json`, which is obsolete.
- **DECISIONS.md:** log the not-yet-logged answer: todo repo backed up to the VPS, not GitHub, with commit-only and manual push. Add conventions: atomic write before delete, the timer's retry, the `commit_inbox` author.
- **HUMAN.md:**
  - Replace step 13 (GitHub repo) with: create a bare repo on the VPS, add it as remote `vps`, and push. Tell me if you'd rather work that one out yourself and have the commands removed.
  - Add the timer install and the new live checks.
  - Update the "Good to know" section.
- **README.md, HANDOFF.md:** describe the new flow.
- Save this plan to `docs/plans/2026-11-08-inbox-file-redesign.md`.
- Commits: code + tests + units, then docs.

## Verification

1. `uv run pytest` passes 4 tests.
2. **Live run (you):**
   - Send 2 messages, one of them multi-line.
   - Run `inbox/inbox pull` from any folder.
   - Check that `inbox.md` has both messages, `git log` in the todo repo shows `inbox: +2 from phone`, and `#inbox` is empty on the phone.
3. Run `pull` again. It prints "nothing new" and makes no new commit.
4. **Timer:**
   - `systemctl --user start inbox-pull.service` performs a pull, and `journalctl --user -u inbox-pull` shows it.
   - `systemctl --user list-timers` lists the next 07:00 run.
5. Open a fresh `claude` session in `~/Documents/todo` and ask what's in the inbox. It answers from `inbox.md` by following AGENTS.md, with no hook involved.
