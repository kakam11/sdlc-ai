---
name: spec-implement
description: Implement exactly one task from an approved tasks.md, mark it complete, and stop to report. Use when the user runs "/spec-implement <slug> [task-number]", asks to implement the next task for a spec, or wants to continue building a spec-driven feature.
---

# spec-implement

Implement one task from a spec's approved task list — no more, no less.

## Steps

1. **Resolve `<slug>`** from the skill argument, same lookup rule as other spec skills (single spec with an approved `tasks.md` that still has unchecked items → use it; multiple → ask).

2. **Read all three docs**: `specs/<slug>/requirements.md`, `design.md`, `tasks.md`. If `tasks.md` doesn't exist, tell the user to run `/spec-tasks` first and stop.

3. **Check approval** on tasks.md (`**Status:** Approved`). If missing, summarize and ask the user to confirm before proceeding, then flip the marker.

4. **Pick the task**:
   - If a task number was given as an argument, use that task (even if already checked — treat it as "redo this one" and tell the user if it was already done).
   - Otherwise, pick the first unchecked (`- [ ]`) task in order.
   - If every task is already checked, tell the user the spec is fully implemented and stop.

5. **Implement exactly that one task.**
   - Use the design doc as the authority for architecture/interfaces, and requirements.md for the behavior each acceptance criterion demands.
   - Write real, working code — no stubs or `TODO` placeholders standing in for the task's actual logic.
   - Write or update tests for the task if the codebase has a test setup, and run them along with any relevant type-check/lint/build step. Fix failures before considering the task done.
   - Do not start on other tasks in the same run, even if they look quick — one task per invocation keeps each change reviewable.

6. **Mark the task complete.** Change its checkbox in `tasks.md` from `- [ ]` to `- [x]`.

7. **Stop and report**: what was implemented, which files changed, what verification was run and its result, and which task (if any) is next. If the task couldn't be fully completed (e.g. a blocking ambiguity or failing test you can't resolve without user input), leave the checkbox unchecked, explain why, and ask rather than guessing.
