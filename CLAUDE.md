# TODO FLOW

## What This Is

A personalized workflow for externalizing my to-do list across personal/academic life. Traditional to-do apps are less-than-helpful to me because they accumulate dust over time and assume a lot about continuity between states. Whan I've found works is essentially a rolling .md file of tasks that I can add to and drop over time with an LLM acting as an executive assistant that helps me to triage working through the list by talking to me about it. See @CLAUDE.todo.md for the instructions for the to-do list (not for you), to understand the use case. This repository is for slowly adding features over time to make that workflow smoother without losing the simplicity of it.

## Specifications

See @SPEC.md for full specs. **Do not edit SPEC.md** -- when changes arise or decisions are made regarding the layout of the app which a human might want to know, instead add to DECISIONS.md.

## Working agreement

I expect this to be a project that evolves over time as I hit friction that is worth fixing. It may sometimes sit for months; it may sometimes get new features in a burst; it may sometimes roll back as things work or don't. Treat this whole project as the plumbing behind the scenes. 

## Architecture Overview

Two machines are primarily involved and should talk to each other:

- My work/personal laptop: System76 Oryx Pro 11 running PopOS Cosmic (this is where I am when I am doing to-do-list relevant tasks)
- My phone: Samsung Galaxy S22 Android (this is where I need to occasionally quickly write down a task and have it show up clean in a markdown file for next time I open the laptop)


## Documentation

- @docs/SPEC.md: original spec as laid out when the project began. Do not edit; keep as an artifact of what the idea started out as so the project remains grounded.
- @docs/HUMAN.md: instructions and notes for the human (Acacia) developer - leave items here when they need human input or steps (e.g. setting up the fly.io server, testing between steps). Like a handoff document and running to-do list for the human. When the human checks items off or tells you they're done, move them from "To-Do" to "Done".
- @docs/HANDOFF.md: instructions and notes for the next Claude instance working on the project. Narrative-style, observational; anything you would want to have next time you start up without memory. Think of it like a teacher's notes for the sub or the video they show the girl at the end of 50 First Dates.
- @docs/DECISIONS.md: A running list of decisions which have a bearing on the design, as a Markdown table with four columns: date, decision, AI contribution, Human contribution. (Either contribution may be empty, if the decision was solely AI or solely human.)
- @docs/plans/: Whenever you enter "plan mode" and produce a plan, when the plan is approved, save it to `plans/YYYY-MM-DD-<plan-title-slug>.md`.
- README.md: Human-facing, written for (depending on the project) both non-coders who want to understand what the tool is and how it's used, and for coders who want to fork and implement. 

Freely update all these documents (except SPEC.md).

## Additional Notes

None currently.