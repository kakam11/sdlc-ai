# Tasks: Reverse String CLI

- [x] 1. Scaffold project and implement grapheme splitting
  - Create `reverse-string-cli/src/Main.java` and `reverse-string-cli/test/MainTest.java`.
  - Implement `static List<String> graphemes(String s)` using `BreakIterator.getCharacterInstance()` to split `s` into grapheme clusters.
  - Add tests: plain ASCII string splits into one cluster per character; a combining-mark sequence (base char + U+0301) splits into a single two-codepoint cluster; empty string splits into an empty list.
  - _Requirements: 1.2_

- [x] 2. Implement string reversal on top of graphemes
  - Implement `static String reverseString(String s)` by concatenating `graphemes(s)` in reverse order.
  - Add tests: `"abc"` → `"cba"`; combining-mark string reverses without splitting the cluster; `""` → `""`.
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 3. Implement argument parsing and usage errors
  - Implement nested `static class UsageException extends RuntimeException` and `static String parseArg(String[] args)`, returning the single argument or throwing `UsageException` for any other arg count.
  - Add tests: one argument returns it; zero args throws `UsageException`; two+ args throws `UsageException`.
  - _Requirements: 2.1, 2.2_

- [x] 4. Wire up `run()`, `main()`, and the CLI entry point
  - Implement `static int run(String[] args, PrintStream out, PrintStream err)`: call `parseArg`, then `reverseString`, print result to `out`; on `UsageException`, print `"Usage: java Main <string>"` to `err` and return `1`; return `0` on success.
  - Implement `public static void main(String[] args)` calling `System.exit(run(args, System.out, System.err))`.
  - Add tests (using `ByteArrayOutputStream`-backed `PrintStream`s): `run(new String[]{"abc"}, ...)` writes `"cba"` to `out` and returns `0`; `run(new String[]{}, ...)` and `run(new String[]{"a","b"}, ...)` write the usage message to `err` and return `1`.
  - _Requirements: 1.1, 2.1, 2.2_

---
**Status:** Approved
