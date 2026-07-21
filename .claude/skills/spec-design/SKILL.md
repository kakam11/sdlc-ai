---
name: spec-design
description: Draft the technical design for a spec whose requirements are approved. Writes specs/<slug>/design.md tied back to the requirements and stops for user approval before tasks are broken out. Use when the user runs "/spec-design", asks to design a feature that already has requirements, or wants to move a spec from requirements to design.
---

# spec-design

Turn approved requirements into a concrete technical design.

## Steps

1. **Resolve `<slug>`** from the skill argument. If not given, look in `specs/` — if there's exactly one spec without a `design.md`, use that; if there are several, ask the user which one.

2. **Read `specs/<slug>/requirements.md`.** If it doesn't exist, tell the user to run `/spec-new` first and stop.

3. **Check approval.** Look for `**Status:** Approved` at the end of requirements.md.
   - If missing or still `Draft`, show the user a short summary of the requirements and ask them to confirm approval before you proceed. Once they confirm, edit requirements.md to set `**Status:** Approved`.
   - Do not draft a design against unapproved requirements without this check.

4. **Write `specs/<slug>/design.md`** with this structure:

   ```markdown
   # Design: <Feature Name>

   ## Overview
   <How this feature works at a high level, and the key design decisions/trade-offs, in a few sentences.>

   ## Architecture
   <Major components/modules and how they interact. Use a short diagram (mermaid or ASCII) only if it clarifies flow — skip if the design is simple enough to describe in prose.>

   ## Components & Interfaces
   <For each component: its responsibility, its public interface (function signatures / API shape / props), and which Requirement(s) it satisfies — e.g. "Satisfies Requirement 2, 3".>

   ## Data Models
   <Key data structures/schemas, only if the feature has meaningful state or persistence. Omit this section if not applicable.>

   ## Error Handling
   <How each error/edge case from the acceptance criteria is handled.>

   ## Testing Strategy
   <What kinds of tests (unit/integration/manual) will verify this, and which requirements they cover.>

   ---
   **Status:** Draft
   ```

   Guidelines:
   - Every meaningful design decision should trace back to a requirement — if you're adding something requirements.md didn't ask for, flag it to the user rather than silently expanding scope.
   - Prefer reusing existing patterns/libraries already in the codebase over introducing new ones; check what's already there before deciding on a stack or approach.
   - Keep it concrete enough that `/spec-tasks` can turn it directly into an implementation checklist — avoid design docs that are just restated requirements.

5. **Stop.** Summarize the design briefly and ask the user to review and approve.
   - On requested changes, edit design.md and ask again.
   - Once approved, set `**Status:** Approved` and tell the user they can now run `/spec-tasks <slug>`.
