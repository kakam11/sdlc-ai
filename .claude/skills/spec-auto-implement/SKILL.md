---
name: spec-auto-implement
description: Implement one task from an approved tasks.md and ship it as a pull request - branch, code, commit, push, open PR - in a single invocation, with the PR itself as the human review gate. Use when the user runs "/spec-auto-implement <slug> [task-number]", or asks to implement a spec task and open a PR / push it to GitHub, as opposed to the local-only "/spec-implement".
---

# spec-auto-implement

Implement one task from a spec's approved task list and open it as a pull request for human review, in one call.

This is the git/GitHub-integrated sibling of `/spec-implement`. Use `/spec-implement` for quick local iteration with no git side effects; use this skill when the task should ship as a reviewable PR. Both check off the same `tasks.md`.

The target repository is never hardcoded here or anywhere else in this project — every git/gh command below operates on whatever the `origin` remote and its default branch currently are. To point at a different repo, the user changes it with `git remote set-url origin <url>` outside this skill; nothing here needs to change.

## Steps

1. **Resolve `<slug>`**, same lookup rule as `/spec-implement`: single spec with an approved `tasks.md` that still has unchecked items → use it; multiple → ask.

2. **Read all three docs**: `specs/<slug>/requirements.md`, `design.md`, `tasks.md`. If `tasks.md` doesn't exist, tell the user to run `/spec-tasks` first and stop.

3. **Check approval** on tasks.md (`**Status:** Approved`). If missing, summarize and ask the user to confirm before proceeding, then flip the marker.

4. **Pick the task**: if a task number was given, use that task; otherwise the first unchecked (`- [ ]`) task in order. If every task is already checked, tell the user the spec is fully implemented and stop.

5. **Sync with the remote before branching**:
   - `git fetch origin`
   - Determine the default branch: `git remote show origin` (look for `HEAD branch:`), falling back to `git ls-remote --symref origin HEAD` if that's inconclusive.
   - `git checkout <default-branch> && git pull origin <default-branch>`
   - If any of this fails (no remote configured, auth failure, network error), stop and tell the user exactly what failed rather than guessing or working around it.

6. **Create the task branch**: `git checkout -b spec/<slug>/task-<n>` off the up-to-date default branch.

7. **Implement exactly that one task** (identical bar to `/spec-implement` step 5): use design.md as the architecture authority and requirements.md for behavior, write real working code (no stubs/TODOs standing in for the logic), write/update tests if the codebase has a test setup, run them plus any relevant type-check/lint/build, and fix failures before continuing.

8. **Check off the task** in `tasks.md` (`- [ ]` → `- [x]`).

9. **Commit**: stage the changed files plus `tasks.md`. Message:
   ```
   <slug>: task <n> - <task title>

   Satisfies requirements: <requirement numbers from the task's _Requirements:_ line>
   ```

10. **Push**: `git push -u origin spec/<slug>/task-<n>`.

11. **Open the PR**: `gh pr create --base <default-branch> --head spec/<slug>/task-<n> --title "<slug>: task <n> - <task title>" --body "<summary of what was implemented, verification run and its result, requirements satisfied>"`.
    - If `gh` isn't installed or isn't authenticated, don't fail silently: tell the user the branch is pushed, give them the compare URL (`<remote-web-url>/pull/new/spec/<slug>/task-<n>`, derived from `origin`'s URL, not a hardcoded host/org), and suggest installing/authenticating `gh` (`gh auth login`, browser-based) if they want this step automated next time.

12. **Stop and report**: the PR URL (or manual-open link), what was implemented, verification results, and which task is next. No further pausing is needed — the open PR is the review gate, same as the "no pause between sub-steps" model this skill was designed for.
