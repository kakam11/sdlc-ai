---
name: spec-status
description: Show a summary of every spec in specs/ - which phase each is in and how many tasks are complete. Use when the user runs "/spec-status" or asks what specs exist, what state they're in, or what's left to implement.
---

# spec-status

Report the state of every spec-driven feature in this workspace.

## Steps

1. If `specs/` doesn't exist or is empty, tell the user no specs exist yet and suggest `/spec-new <feature description>` to start one. Stop.

2. For each subdirectory of `specs/`, determine:
   - **Phase**: the furthest doc that exists and its status —
     - no `requirements.md` → shouldn't happen, skip/flag
     - `requirements.md` present, not Approved → `requirements (draft)`
     - `requirements.md` Approved, no `design.md` → `requirements (approved)`
     - `design.md` present, not Approved → `design (draft)`
     - `design.md` Approved, no `tasks.md` → `design (approved)`
     - `tasks.md` present, not Approved → `tasks (draft)`
     - `tasks.md` Approved, 0 tasks checked → `ready to implement`
     - `tasks.md` Approved, some but not all checked → `implementing`
     - `tasks.md` Approved, all checked → `done`
   - **Progress**: count of `- [x]` vs total `- [ ]`/`- [x]` lines in `tasks.md` (e.g. `3/8`), if it exists.

3. Print a compact table, one row per spec, columns: **Spec**, **Phase**, **Progress**. Sort by least-complete first (drafts and in-progress specs before done ones) so what needs attention surfaces at the top.

4. After the table, name the single most actionable next step overall (e.g. "`design-x` requirements are still a draft — review and approve them to unblock design", or "`feature-y` has 2 unchecked tasks — run `/spec-implement feature-y` to continue").
