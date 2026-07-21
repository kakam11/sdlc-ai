---
name: spec-new
description: Start a new spec-driven feature. Creates specs/<slug>/requirements.md with EARS-style acceptance criteria and stops for user approval before any design or code work begins. Use when the user wants to begin spec-driven development on a new feature, says "/spec-new", or asks to "start a new spec".
---

# spec-new

Kick off the requirements phase of spec-driven development for one feature.

## Steps

1. **Determine the feature description** from the skill argument. If none was given, or it's too vague to write concrete requirements from, ask the user directly (plain question, not a whole interview) before writing anything.

2. **Slugify** the feature name into `kebab-case` (lowercase, spaces/punctuation → hyphens). This is `<slug>`.

3. Check whether `specs/<slug>/` already exists.
   - If it exists and has a `requirements.md`, tell the user and ask whether they want to revise it or pick a different slug. Do not silently overwrite.
   - Otherwise create `specs/<slug>/`.

4. **Write `specs/<slug>/requirements.md`** with this structure:

   ```markdown
   # Requirements: <Feature Name>

   ## Introduction
   <2-4 sentences: what this feature is, who it's for, why it's being built.>

   ## Requirements

   ### Requirement 1: <short name>
   **User Story:** As a <role>, I want <capability>, so that <benefit>.

   #### Acceptance Criteria
   1. WHEN <event/trigger> THE SYSTEM SHALL <expected behavior>
   2. IF <precondition> THEN THE SYSTEM SHALL <expected behavior>
   3. WHEN <error/edge case> THE SYSTEM SHALL <expected behavior>

   ### Requirement 2: <short name>
   ... (repeat per distinct capability)

   ---
   **Status:** Draft
   ```

   Guidelines for good requirements:
   - Each Requirement should cover one distinct capability, not a whole feature at once.
   - Acceptance criteria use EARS syntax (`WHEN ... THE SYSTEM SHALL ...`, `IF ... THEN THE SYSTEM SHALL ...`) so they're testable, not vague.
   - Include edge cases and error conditions as their own acceptance criteria — don't only cover the happy path.
   - Don't invent scope the user didn't ask for. If genuinely unsure about a boundary (e.g. auth, persistence, concurrency), ask rather than guessing.

5. **Stop.** Tell the user the requirements are drafted at `specs/<slug>/requirements.md`, summarize the requirements briefly, and ask them to review and approve.
   - If they ask for changes, edit the file and ask again.
   - Once they approve, edit the file's final line to `**Status:** Approved` and tell them they can now run `/spec-design <slug>`.
   - Do not proceed to design or implementation yourself in this same turn — the next phase is a separate, deliberate step.
