# TITLE OF PROJECT

## What This Is

[description of project, 4-5 sentences max]

## Specifications

See @SPEC.md for full specs. **Do not edit SPEC.md** -- when changes arise or decisions are made regarding the layout of the app which a human might want to know, instead add to DECISIONS.md.

## Working agreement

[norms & goals to follow for the project - e.g., "The goal is something that just works"; "Must be securely robust to injection attacks"; things like that.]

## Architecture Overview

[begin with any initial constraints on stack or deployment; fills in over time as the project is built]

## Documentation

- @docs/SPEC.md: original spec as laid out when the project began. Do not edit; keep as an artifact of what the idea started out as so the project remains grounded.
- @docs/HUMAN.md: instructions and notes for the human (Acacia) developer - leave items here when they need human input or steps (e.g. setting up the fly.io server, testing between steps). Like a handoff document and running to-do list for the human. When the human checks items off or tells you they're done, move them from "To-Do" to "Done".
- @docs/HANDOFF.md: instructions and notes for the next Claude instance working on the project. Narrative-style, observational; anything you would want to have next time you start up without memory. Think of it like a teacher's notes for the sub or the video they show the girl at the end of 50 First Dates.
- @docs/DECISIONS.md: A running list of decisions which have a bearing on the design, as a Markdown table with four columns: date, decision, AI contribution, Human contribution. (Either contribution may be empty, if the decision was solely AI or solely human.)
- @docs/plans/: Whenever you enter "plan mode" and produce a plan, when the plan is approved, save it to `plans/YYYY-MM-DD-<plan-title-slug>.md`.
- README.md: Human-facing, written for (depending on the project) both non-coders who want to understand what the tool is and how it's used, and for coders who want to fork and implement. 

Freely update all these documents (except SPEC.md).

## Additional Notes

[any notes or additional things you want claude to know at the outset of a project or on each turn]