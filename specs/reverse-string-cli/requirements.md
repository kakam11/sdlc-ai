# Requirements: Reverse String CLI

## Introduction
A small command-line tool that takes a single string argument and prints it reversed to stdout. Intended as a minimal utility/example, used directly from a terminal.

## Requirements

### Requirement 1: Reverse the input string
**User Story:** As a terminal user, I want to pass a string as a command-line argument, so that I can quickly see it reversed without writing any code.

#### Acceptance Criteria
1. WHEN the tool is run with exactly one argument THE SYSTEM SHALL print that argument's characters in reverse order to stdout, followed by a newline.
2. WHEN the argument contains unicode characters (e.g. accented letters, emoji) THE SYSTEM SHALL reverse it by user-perceived characters (grapheme clusters), not raw code units, so multi-byte characters aren't corrupted.
3. WHEN the argument is an empty string THE SYSTEM SHALL print an empty line (no error).

### Requirement 2: Handle invalid invocations
**User Story:** As a terminal user, I want clear feedback when I use the tool incorrectly, so that I know how to fix my command.

#### Acceptance Criteria
1. IF the tool is run with zero arguments THEN THE SYSTEM SHALL print a usage message to stderr and exit with a non-zero status code.
2. IF the tool is run with more than one argument THEN THE SYSTEM SHALL print a usage message to stderr and exit with a non-zero status code.

---
**Status:** Approved
