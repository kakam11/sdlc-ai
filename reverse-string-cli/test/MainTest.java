import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class MainTest {

    @Test
    void graphemesSplitsAsciiIntoOneClusterPerChar() {
        assertEquals(List.of("a", "b", "c"), Main.graphemes("abc"));
    }

    @Test
    void graphemesKeepsCombiningMarkWithBaseChar() {
        // 'e' (U+0065) followed by a combining acute accent (U+0301): two codepoints, one grapheme cluster.
        String eWithCombiningAcute = "é";
        assertEquals(List.of(eWithCombiningAcute), Main.graphemes(eWithCombiningAcute));
    }

    @Test
    void graphemesOfEmptyStringIsEmptyList() {
        assertEquals(List.of(), Main.graphemes(""));
    }

    @Test
    void reverseStringReversesAsciiCharacters() {
        assertEquals("cba", Main.reverseString("abc"));
    }

    @Test
    void reverseStringDoesNotSplitCombiningMarkCluster() {
        // 'e' (U+0065) followed by a combining acute accent (U+0301), sandwiched between plain letters.
        String input = "a" + "é" + "b";
        String reversed = Main.reverseString(input);
        assertEquals(List.of("b", "é", "a"), Main.graphemes(reversed));
    }

    @Test
    void reverseStringOfEmptyStringIsEmptyString() {
        assertEquals("", Main.reverseString(""));
    }

    @Test
    void parseArgReturnsTheSingleArgument() {
        assertEquals("hello", Main.parseArg(new String[]{"hello"}));
    }

    @Test
    void parseArgThrowsUsageExceptionForZeroArgs() {
        assertThrows(Main.UsageException.class, () -> Main.parseArg(new String[]{}));
    }

    @Test
    void parseArgThrowsUsageExceptionForTooManyArgs() {
        assertThrows(Main.UsageException.class, () -> Main.parseArg(new String[]{"a", "b"}));
    }

    @Test
    void runPrintsReversedStringAndReturnsZero() {
        ByteArrayOutputStream outBytes = new ByteArrayOutputStream();
        ByteArrayOutputStream errBytes = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(outBytes, true, StandardCharsets.UTF_8);
        PrintStream err = new PrintStream(errBytes, true, StandardCharsets.UTF_8);

        int exitCode = Main.run(new String[]{"abc"}, out, err);

        assertEquals(0, exitCode);
        assertEquals("cba" + System.lineSeparator(), outBytes.toString(StandardCharsets.UTF_8));
        assertEquals("", errBytes.toString(StandardCharsets.UTF_8));
    }

    @Test
    void runWithZeroArgsWritesUsageToErrAndReturnsOne() {
        ByteArrayOutputStream outBytes = new ByteArrayOutputStream();
        ByteArrayOutputStream errBytes = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(outBytes, true, StandardCharsets.UTF_8);
        PrintStream err = new PrintStream(errBytes, true, StandardCharsets.UTF_8);

        int exitCode = Main.run(new String[]{}, out, err);

        assertEquals(1, exitCode);
        assertEquals("Usage: java Main <string>" + System.lineSeparator(), errBytes.toString(StandardCharsets.UTF_8));
        assertEquals("", outBytes.toString(StandardCharsets.UTF_8));
    }

    @Test
    void runWithTooManyArgsWritesUsageToErrAndReturnsOne() {
        ByteArrayOutputStream outBytes = new ByteArrayOutputStream();
        ByteArrayOutputStream errBytes = new ByteArrayOutputStream();
        PrintStream out = new PrintStream(outBytes, true, StandardCharsets.UTF_8);
        PrintStream err = new PrintStream(errBytes, true, StandardCharsets.UTF_8);

        int exitCode = Main.run(new String[]{"a", "b"}, out, err);

        assertEquals(1, exitCode);
        assertEquals("Usage: java Main <string>" + System.lineSeparator(), errBytes.toString(StandardCharsets.UTF_8));
        assertEquals("", outBytes.toString(StandardCharsets.UTF_8));
    }
}
