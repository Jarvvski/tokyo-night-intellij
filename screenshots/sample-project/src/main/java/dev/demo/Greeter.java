package dev.demo;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Formats greetings for a list of names.
 *
 * @author Ada Lovelace
 */
public final class Greeter {

    private static final String GREETING = "Hello";

    private static final String TEMPLATE = """
            %s!
            Have a productive session.
            """;

    private final boolean excited;

    public Greeter(boolean excited) {
        this.excited = excited;
        // TODO(tokyo-night): localise punctuation per locale.
        assert GREETING != null;
    }

    public String greet(List<String> names) {
        return names.stream()
                .filter(name -> !name.isBlank())
                .map(this::format)
                .collect(Collectors.joining(System.lineSeparator()));
    }

    private String format(String name) {
        String greeting = GREETING + ", " + name;
        return excited ? greeting.toUpperCase() : greeting;
    }

    @Override
    public String toString() {
        return String.format(TEMPLATE.strip(), GREETING);
    }
}
