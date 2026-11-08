# todo-flow

I like keeping my to-do list in a plain markdown file that I can access and work with in an LLM (this is helpful to me because I work better when my to-do list happens as a body doubling conversation), but I also like being able to quickly note something down on my phone when a new task comes up. 

I didn't want to create a new app to do this (hasn't worked in the past) or did I want to edit the markdown file directly from my phone (not for any logical reason. I just find it more helpful to send future to-dos as messages to actually clear them from my brain space).

This repo is my current best solution to that problem and is intended only for me specifically to use. You can steal any of it that you want to, though, if you would also find some of this helpful.

## Workflow: Discord Inbox

- I have a private Discord server with a channel `#inbox` where I message future-me about what to do.
- At 7 AM or when my laptop starts, whichever comes later (almost always the laptop start), an automatic trigger dumps it into an `.md` file in my to-do list folder on my laptop. 
  - Whenever it reads from the channel it also deletes the message from the channel; this is **not** a persistent list, more like sticky notes
  - I can also just type `inbox pull` into the terminal from wherever and it'll do the above manually
- I can start a conversation with an LLM (usually Claude in my case) in the to-do list folder and it'll read from both my nice, pretty, finalized to-do list and my messy, scribbled, auto-read inbox 

## How-It's-Made for People Who Care

(Human-readable section of README)

- Primarily Claude-coded; see commit history & [DECISIONS.md](docs/DECISIONS.md) for details 
- `inbox/inbox.py pull` does this (symlinked into `~/.local/bin` so I can `inbox pull` from wherever)
  - reads the channel through Discord's REST API with a bot token
  - appends new messages to `inbox.md` (written to a temp file and swapped in, deduped by a hidden `<!-- discord:ID -->` marker per entry
  - commits the file
  - deletes the messages from Discord
- `deploy/` is set up as a systemd user service:
  - daily 07:00 run (arbitrarily chosen by Claude, I could probably make this 09:00 or something reasonable)
  - catches up on wake 
  - retry every minute (up to 5 tries) if the network isn't up yet

Setup:

Make a discord bot with the following permissions:

  - Installation tab:
    - **Turn off** Install Link (you will get one later)
  - Bot tab:
    - Reset token: grab your token and SAVE IT SOMEWHERE
    - Authorization Flow permissions:
      - **Turn off** Public bot
      - **Turn on** Message Content Intent
  - OAuth2 tab:
    - click **bot**
    - select:
      - View Channels
      - Read Message History
      - Manage Messages

Copy `.env.example` to `.env` and put in your bot token (did you save it?) and your channel ID where you're sending messages (right click the channel name; need Developer permissions).

Tests: `uv run pytest`.

## How-It's-Made for Bots who Need to Know

(This is for the robots)

Orientation for an agent working in or forking this repo. Read it before changing anything under `inbox/`.

**The invariant.** A note must always exist somewhere: in Discord until it's safely written to `inbox.md`, and in `inbox.md` until it's filed into a week file. Every ordering choice in `cmd_pull` serves this, so keep it intact.

- Order is write (temp file + `os.replace`), then commit, then delete. Never delete from Discord before the write succeeds.
- `pull` only appends. It never rewrites or removes existing `inbox.md` content; removing entries is the reader's job.
- Messages with no text stay in Discord. That covers photos, and also every message when Message Content Intent is off, in which case they all arrive blank.
- A failed delete is harmless: the ID marker prevents a duplicate on the next run.

**The `inbox.md` contract.** The file is read by people and by arbitrary LLMs, following `AGENTS.md` in the private todo repo (not in this repo).

- Entry format: `- Sun Nov 8, 9:14 PM: first line <!-- discord:<message id> -->`. Continuation lines are indented two spaces.
- `<!-- discord:(\d+) -->` is the dedupe key. If you change the format, migrate existing entries, or messages will be added twice.
- `HEADER` is written only when the file is created.

**Map.**

- `inbox/inbox`: bash wrapper. It resolves its own symlink with `readlink -f`, then runs `inbox.py` via `uv run --project <repo root>`.
- `inbox/inbox.py`: all the logic. The seams the tests replace are `load_config`, `fetch_messages`, `delete_message`, `add_to_inbox`, `commit_inbox`.
- `.env` (gitignored) sits at the repo root and is found relative to the script, not the working directory. `INBOX_FILE` is optional and defaults to `~/Documents/todo/inbox.md`.
- `deploy/`: systemd user units. `ExecStart` is an absolute path. Install with `systemctl --user link` on both files, then `systemctl --user enable --now inbox-pull.timer`.
- `tests/test_inbox.py`: 4 tests, no network, no git. Keep the test count proportionate to the stakes; this is a personal tool.

**Exit codes.** `pull` exits:

- 0 on success, including "nothing new" and textless messages skipped
- 1 if Discord is unreachable, the write fails, or any delete fails
- 2 on bad usage

The systemd `Restart=on-failure` retry depends on that 1, so don't turn failures into exit 0.

**Deliberately absent. Ask Acacia before adding any of these:**

- A gateway connection, always-on bot, or VPS service. The bot showing "offline" is correct.
- Pushing from `pull`. It commits only; she pushes by hand.
- Any LLM step in the timer. A morning pre-sort idea is parked in `docs/HUMAN.md`.
- Anything Claude-specific in the inbox path. It has to stay LLM-agnostic. An earlier version used a SessionStart hook and an `ack` command, and was replaced the same day (see DECISIONS.md).
- Attachments.

**Discord API notes.**

- It uses REST v10 with `Authorization: Bot <token>`.
- Messages come back newest first, paginated with `before`. Message IDs (snowflakes) sort chronologically.
- Types 0 and 19 are user messages; everything else is skipped.
- On a 429, `retry_after` is honored: at most 3 tries, waiting at most 10 seconds.
- Message content needs the privileged intent even over REST.

**Working here.** Follow `CLAUDE.md`:

- `docs/SPEC.md` is frozen.
- Log decisions in `docs/DECISIONS.md`, with who contributed what.
- Steps a human has to do go in `docs/HUMAN.md`.
- Notes for the next agent go in `docs/HANDOFF.md`.
- Keep commits small, authored as yourself.

**If forking:**

- Change `ExecStart` in `deploy/inbox-pull.service`.
- Set `INBOX_FILE`, and adjust `HEADER`, which names Acacia.
- Give the LLM in your todo folder the rule "remove an entry only after it's filed."
- `strftime("%-d")` works on Linux and macOS but not Windows.

## Docs

- [docs/SPEC.md](docs/SPEC.md): the original (deliberately thin) spec
- [docs/DECISIONS.md](docs/DECISIONS.md): what got decided, and by whom
- [docs/HUMAN.md](docs/HUMAN.md): setup steps and to-dos for me
- [docs/HANDOFF.md](docs/HANDOFF.md): notes for the next Claude session
- [docs/plans/](docs/plans/): approved build plans

Templated from [cc-template](https://github.com/alackles/cc-template).