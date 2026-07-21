# Design: Reverse String CLI

## Overview
A single small Java class with no external dependencies, run via the JDK directly (`java Main.java <string>` or compiled with `javac`). Grapheme-safe reversal is done with `java.text.BreakIterator.getCharacterInstance()`, the JDK's built-in Unicode grapheme-cluster boundary logic, so combining marks and multi-codepoint characters aren't split incorrectly.

## Architecture
```
reverse-string-cli/
  src/
    Main.java          # CLI entry point + all logic (small enough not to split further)
  test/
    MainTest.java       # unit tests
```
`Main.java` is invoked as `java Main.java <string>` (JDK 11+ single-file source launch) or compiled+run as a regular class. Flow: parse `args` → validate arg count → split into grapheme clusters via `BreakIterator` → reverse → print.

## Components & Interfaces

**`static String parseArg(String[] args)`**
- Returns the single string argument.
- Throws `UsageException` if `args.length != 1`.
- Satisfies Requirement 2.1, 2.2.

**`static List<String> graphemes(String s)`**
- Splits `s` into a list of grapheme clusters using `BreakIterator.getCharacterInstance()`: iterate boundaries and substring between each pair.
- Satisfies Requirement 1.2.

**`static String reverseString(String s)`**
- Builds the reversed string by concatenating `graphemes(s)` in reverse order.
- Satisfies Requirement 1.1, 1.3 (empty string → `graphemes("")` is empty list → `""`).

**`static int run(String[] args, PrintStream out, PrintStream err)`**
- Calls `parseArg`, then `reverseString`, prints result to `out` with a trailing newline.
- On `UsageException`, prints `"Usage: java Main <string>"` to `err` and returns `1`.
- Returns `0` on success.
- Satisfies Requirement 1.1, 2.1, 2.2.
- Taking `PrintStream` params (rather than hardcoding `System.out`/`System.err`) keeps `run` testable without capturing real stdout/stderr.

**`public static void main(String[] args)`**
- Calls `System.exit(run(args, System.out, System.err))`.

`UsageException` is a small `static class UsageException extends RuntimeException` nested in `Main`.

## Data Models
None — the tool is stateless; no persistence.

## Error Handling
- Zero args or 2+ args → `UsageException` → usage message on stderr, exit code `1` (Requirement 2.1, 2.2).
- No other error conditions exist (any string, including empty, is valid input per Requirement 1.3).

## Testing Strategy
Unit tests (JUnit 5) directly against `reverseString`, `graphemes`, `parseArg`, and `run` (passing `PrintStream`s backed by `ByteArrayOutputStream` to capture output):
- `"abc"` → `"cba"` (Requirement 1.1)
- string with a combining accent (e.g. `"e"` + combining acute, U+0301) reverses as one cluster, not split (Requirement 1.2)
- `""` → `""` (Requirement 1.3)
- `run(new String[]{}, ...)` and `run(new String[]{"a","b"}, ...)` → return `1` and write a usage message to the error stream (Requirement 2.1, 2.2)

---
**Status:** Approved
