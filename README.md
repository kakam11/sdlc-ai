# Spec-Driven Development

A set of Claude Code skills that walk any feature through four gated phases —
**requirements → design → tasks → implementation** — so nothing gets built
before there's an approved spec behind it.

## Workflow

```
/spec-new "<feature description>"         → specs/<slug>/requirements.md   (stops for approval)
/spec-design <slug>                       → specs/<slug>/design.md         (stops for approval)
/spec-tasks <slug>                        → specs/<slug>/tasks.md          (stops for approval)
/spec-implement <slug> [task-number]      → implements one task locally, checks it off, repeat
/spec-auto-implement <slug> [task-number] → implements one task, opens it as a PR, repeat
/spec-status                              → progress across every spec
```

Each phase reads the previous doc(s) and won't proceed until the prior one is
marked approved — Claude will ask you to review and confirm before flipping
that marker itself. `/spec-implement` does exactly one task per run and stops
to report, so every change stays reviewable; call it again to move to the
next task. `/spec-auto-implement` is the git/GitHub-integrated sibling: same
one-task-per-run model, but it also branches, commits, pushes, and opens a
pull request — the PR itself is the review gate, so it doesn't pause before
that point.

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
- `/spec-auto-implement` puts each task on its own branch,
  `spec/<slug>/task-<n>`, and opens one PR per task rather than batching a
  whole spec into a single PR.

## Git/GitHub integration

- **Target repo is whatever `origin` is set to** — never hardcoded in any
  skill or doc here. Point this workflow at a different repo any time with
  `git remote set-url origin <url>`; nothing in `.claude/skills/` needs to
  change.
- Requires the `gh` CLI installed and authenticated (`gh auth login`) for
  `/spec-auto-implement` to open PRs automatically. Without it, the skill
  still branches, commits, and pushes, then gives you a manual PR-compare
  link instead of failing silently.

## Skills

| Command | What it does |
|---|---|
| `/spec-new` | Drafts `requirements.md` for a new feature. |
| `/spec-design` | Drafts `design.md` from approved requirements. |
| `/spec-tasks` | Drafts `tasks.md` from an approved design. |
| `/spec-implement` | Implements one task at a time, locally, no git side effects. |
| `/spec-auto-implement` | Implements one task and ships it as a pull request. |
| `/spec-status` | Shows phase and task progress for every spec. |

These skills are project-local (`.claude/skills/`) — they only apply inside
this workspace.
