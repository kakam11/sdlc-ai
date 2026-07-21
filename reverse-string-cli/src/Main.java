import java.io.PrintStream;
import java.text.BreakIterator;
import java.util.ArrayList;
import java.util.List;

public class Main {

    static List<String> graphemes(String s) {
        List<String> result = new ArrayList<>();
        BreakIterator iterator = BreakIterator.getCharacterInstance();
        iterator.setText(s);
        int start = iterator.first();
        for (int end = iterator.next(); end != BreakIterator.DONE; start = end, end = iterator.next()) {
            result.add(s.substring(start, end));
        }
        return result;
    }

    static String reverseString(String s) {
        List<String> clusters = graphemes(s);
        StringBuilder builder = new StringBuilder();
        for (int i = clusters.size() - 1; i >= 0; i--) {
            builder.append(clusters.get(i));
        }
        return builder.toString();
    }

    static class UsageException extends RuntimeException {
    }

    static String parseArg(String[] args) {
        if (args.length != 1) {
            throw new UsageException();
        }
        return args[0];
    }

    static int run(String[] args, PrintStream out, PrintStream err) {
        try {
            String arg = parseArg(args);
            out.println(reverseString(arg));
            return 0;
        } catch (UsageException e) {
            err.println("Usage: java Main <string>");
            return 1;
        }
    }

    public static void main(String[] args) {
        System.exit(run(args, System.out, System.err));
    }
}
