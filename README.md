# Spec-Driven Development

A set of Claude Code skills that walk any feature through four gated phases —
**requirements → design → tasks → implementation** — so nothing gets built
before there's an approved spec behind it.

## Workflow

```
/spec-new "<feature description>"    → specs/<slug>/requirements.md   (stops for approval)
/spec-design <slug>                  → specs/<slug>/design.md         (stops for approval)
/spec-tasks <slug>                   → specs/<slug>/tasks.md          (stops for approval)
/spec-implement <slug> [task-number] → implements one task, checks it off, repeat
/spec-status                         → progress across every spec
```

Each phase reads the previous doc(s) and won't proceed until the prior one is
marked approved — Claude will ask you to review and confirm before flipping
that marker itself. `/spec-implement` does exactly one task per run and stops
to report, so every change stays reviewable; call it again to move to the
next task.

## Conventions

- Every feature lives in `specs/<slug>/`, where `<slug>` is the kebab-case
  feature name.
- Each doc (`requirements.md`, `design.md`, `tasks.md`) ends with a
  `**Status:** Draft` / `**Status:** Approved` marker — that's the whole
  approval mechanic, no extra tooling required.
- `requirements.md` uses EARS-style acceptance criteria
  (`WHEN <event> THE SYSTEM SHALL <behavior>`).
- `tasks.md` is a markdown checklist; each task cites the requirement
  number(s) it satisfies for traceability.

## Skills

| Command | What it does |
|---|---|
| `/spec-new` | Drafts `requirements.md` for a new feature. |
| `/spec-design` | Drafts `design.md` from approved requirements. |
| `/spec-tasks` | Drafts `tasks.md` from an approved design. |
| `/spec-implement` | Implements one task at a time from approved tasks. |
| `/spec-status` | Shows phase and task progress for every spec. |

These skills are project-local (`.claude/skills/`) — they only apply inside
this workspace.
