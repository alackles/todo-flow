# Claude Code Templating

This is a template for Claude Code driven projects. Over time I've developed a project workflow that I'm pretty happy with, so I wanted to place it onto GitHub as a template to share with colleagues and students.

You can take whatever you want from here and use it however you want. Not all of it will be of equal use to you.

## What's In It

- `CLAUDE.md`: per-project orchestrating document telling Claude how to use the files listed below and also explaining what you want
- `docs/DECISIONS.md`: log of how you used AI in the project and what choices were made
- `docs/HANDOFF.md`: space for Claude to write to itself that is less structured than anywhere else; like scratch space that persists
- `docs/HUMAN.md`: a place for you to reference what on earth your agent told you to do or what steps you're supposed to take next
- `docs/SPEC.md`: the frozen initial spec that you wanted before scope creep set in

Also comes with templates based off 2 of my custom output styles (but see note at bottom):
- `.claude/output-styles/TEMPLATE-hobby`: focused on making stuff that "just works"
- `claude/output-styles/TEMPLATE-scholarly`: focused on reproducible provenance-first academic & scholarly work

## Why You Might Want To Use It

Good for:
- People who like making custom "stuff" for their classes and research and don't mind putting in a little bit of time up-front to do so (less time, in my experience, than I have ever spent making custom "stuff" in the past)
- People who are concerned about what percentage of their thinking they are doing versus that AI is doing and how to demonstrate that percentage to reviewers or other evaluators
- People who feel like they want a lot of fine grained control over their AI workflow
- People who get annoyed about AI making stuff that lives entirely inside ephemeral or proprietary systems and want to nudge it in the other direction

Bad for:
- People who need to make things at production scale
- People whose favorite part of making "stuff" is figuring out why the "stuff" is broken (AI is very good at doing this, so you will not get the satisfaction of doing it yourself most of the time)
- People who do not want to think much about what it is they are making (these templates make your AI ask a lot of questions)
- People who don't like when their AI talks to them like it might have subjective opinions (these templates explicitly encourage it to do so)

## Features

As a suite, this workflow...

Prioritizes:
- Making stuff that works rather than making stuff that is robust
- Personalized use cases rather than generalized use cases
- Concept before implementation -- primarily asks to plan/draft before implementing and for approval on each step
- Provenance of ideas -- did you do that, or did the AI do that, or did you do it together, or some secret fourth thing?
- Frequent logging of chances and decisions -- prioritize small commits with the agent handling provenance for you
- Reusable code -- encourages agents to write and retain scripts instead of creating ghost code that vanishes into the aether 
- Single-channel workflow -- discourages deployment of sub-agents
- Opinionated agents -- tries to get your Claude to give you its real opinion by telling it you value its input (only works if you actually value its input)

Deprioritizes:
- Excessive testing
- Efficiency

## Example Repos

Here are some projects I've built with this workflow. Will add as I keep making them.

- [you-annotate](https://github.com/alackles/you-annotate): An annotation platform for collaborative classroom annotating. Spec to working model in-classroom in roughly 3 hours.

## Helpful Hints

- I usually use Claude.ai to draft the initial CLAUDE.md and SPEC.md by going back and forth chatting with it for a while about what I want and then telling it I'd like to hand it off to Claude Code. This tends to produce a nice structured result for me to jump off from because I've hammered out a lot of the ambiguities through talking it through.
- Using Plan Mode at the start of a project, and then saving that plan, produces far better results than asking Claude to just start doing something, **even if you make no edits to the plan**. Forcing it to think through its own plan first before implementing it creates a series of structured steps upon which it can act.

## Note on Output Styles

The output styles provided in here are edited/redacted versions of my own personal output styles for Claude Code. My versions have been shaped over time and personalized for my own use cases and the redactions probably contain most of the pieces I find most helpful, but which would not apply to you. So, if you aren't me and you're using the provided output styles as templates, your mileage may vary.

The best output style is the one that you like the best.
