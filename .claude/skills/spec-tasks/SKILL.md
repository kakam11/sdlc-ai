---
name: spec-tasks
description: Break an approved design into an ordered, checkable implementation task list at specs/<slug>/tasks.md, then stop for user approval before any code is written. Use when the user runs "/spec-tasks", asks to plan out tasks for a designed feature, or wants to move a spec from design to an implementation checklist.
---

# spec-tasks

Turn an approved design into a concrete, ordered checklist of coding tasks.

## Steps

1. **Resolve `<slug>`** from the skill argument, same lookup rule as other spec skills (single spec with a `design.md` but no `tasks.md` → use it; multiple → ask).

2. **Read `specs/<slug>/requirements.md` and `specs/<slug>/design.md`.** If design.md doesn't exist, tell the user to run `/spec-design` first and stop.

3. **Check approval** on design.md (`**Status:** Approved`). If missing, summarize the design and ask the user to confirm before proceeding, then flip the marker.

4. **Write `specs/<slug>/tasks.md`** with this structure:

   ```markdown
   # Tasks: <Feature Name>

   - [ ] 1. <Concrete task title>
     - <what to build/change, specific enough to act on>
     - _Requirements: 1.1, 1.2_

   - [ ] 2. <Concrete task title>
     - <details>
     - _Requirements: 2.1_

   ...

   ---
   **Status:** Draft
   ```

   Guidelines for good tasks:
   - Each task should be small enough to implement and verify in one sitting, and should build on prior tasks (no forward references to code that doesn't exist yet).
   - Order tasks so the codebase stays in a working state after each one — favor a walking skeleton (scaffolding → core logic → edge cases → polish) over building unrelated pieces in parallel.
   - Prefer writing the test for a piece of behavior in the same task (or the task immediately before) the behavior that it verifies.
   - Every task should cite the specific requirement number(s) it satisfies (from requirements.md's numbered acceptance criteria) so traceability is clear.
   - Don't include non-coding tasks (deployment, user acceptance testing, documentation-only tasks) unless the user's requirements explicitly called for them.

5. **Stop.** Summarize the task list briefly and ask the user to review and approve.
   - On requested changes, edit tasks.md and ask again.
   - Once approved, set `**Status:** Approved` and tell the user they can now run `/spec-implement <slug>` to start building.
