# Spec-Driven Development

A set of Claude Code skills that walk any feature through four gated phases —
**requirements → design → tasks → implementation** — so nothing gets built
before there's an approved spec behind it.

## Workflow

```
/spec-new "<feature description>"    → specs/<slug>/requirements.md   (stops for approval)
/spec-design <slug>                  → specs/<slug>/design.md         (stops for approval)
/spec-tasks <slug>                   → specs/<slug>/tasks.md          (stops for approval)
/spec-implement <slug> [task-number] → implements one task locally, checks it off, repeat
/spec-status                         → progress across every spec
```

Each phase reads the previous doc(s) and won't proceed until the prior one is
marked approved — Claude will ask you to review and confirm before flipping
that marker itself. `/spec-implement` does exactly one task per run and stops
to report, so every change stays reviewable; call it again to move to the
next task.

For shipping a task as a pull request instead of a local-only change, ask
Claude to use the **`spec-auto-implement` agent** (there's no slash command
for this one — invoke it by name, e.g. "use the spec-auto-implement agent to
do task 2 of reverse-string-cli and open a PR", the same way you'd ask for
the `Explore` or `Plan` agent). It runs isolated in its own git worktree and
in the background, so the main session stays free while it branches, codes,
commits, pushes, and opens the PR — the PR itself is the review gate, so it
doesn't pause before that point.

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
- The `spec-auto-implement` agent puts each task on its own branch,
  `spec/<slug>/task-<n>`, and opens one PR per task rather than batching a
  whole spec into a single PR.

## Git/GitHub integration

- **Target repo is whatever `origin` is set to** — never hardcoded in any
  skill, agent, or doc here. Point this workflow at a different repo any
  time with `git remote set-url origin <url>`; nothing under `.claude/`
  needs to change.
- Requires the `gh` CLI installed and authenticated (`gh auth login`) for
  the `spec-auto-implement` agent to open PRs automatically. Without it, it
  still branches, commits, and pushes, then gives you a manual PR-compare
  link instead of failing silently.

## Skills

| Command | What it does |
|---|---|
| `/spec-new` | Drafts `requirements.md` for a new feature. |
| `/spec-design` | Drafts `design.md` from approved requirements. |
| `/spec-tasks` | Drafts `tasks.md` from an approved design. |
| `/spec-implement` | Implements one task at a time, locally, no git side effects. |
| `/spec-status` | Shows phase and task progress for every spec. |

These skills are project-local (`.claude/skills/`) — they only apply inside
this workspace.

## Agents

| Agent | What it does |
|---|---|
| `spec-auto-implement` | Implements one task and ships it as a pull request; runs isolated (its own git worktree) and in the background. Invoke by name, not a slash command. |

Defined in `.claude/agents/` — also project-local. **New `.claude/agents/`
directories need a Claude Code restart before the agent is picked up**, the
same restart that was needed the first time `.claude/skills/` was created.
