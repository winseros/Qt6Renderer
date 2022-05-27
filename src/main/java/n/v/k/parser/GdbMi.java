package n.v.k.parser;

import org.jetbrains.annotations.NotNull;

import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.Objects;

public class GdbMi {
    private List<GdbMi> children = Collections.emptyList();
    private String name;
    private String data;
    private GdbMiType type = GdbMiType.Invalid;

    public void fromStringMultiple(@NotNull String data) {
        var parser = new DebugOutputParser(data);
        parseTupleHelper(parser);
    }

    public void fromString(@NotNull String data) {
        var parser = new DebugOutputParser(data);
        parseResultOrValue(parser);
    }

    public GdbMi getChild(@NotNull String name) {
        for (GdbMi child : children) {
            if (Objects.equals(child.name, name))
                return child;
        }
        return null;
    }

    public int size() {
        return children.size();
    }

    public GdbMi get(int n) {
        return children.get(n);
    }

    private void parseResultOrValue(@NotNull DebugOutputParser parser) {
        parser.skipCommas();
        if (parser.isAtEnd())
            return;

        parseValue(parser);
        parser.skipSpaces();

        if (isValid() || parser.isAtEnd())
            return;

        if (parser.isCurrent('(')) {
            parser.advance();
            return;
        }

        name = parser.readString(this::isNameChar);

        if (!parser.isAtEnd() && parser.isCurrent('=')) {
            parser.advance();
            parseValue(parser);
        }
    }

    private void parseValue(@NotNull DebugOutputParser parser) {
        if (parser.isAtEnd())
            return;

        switch (parser.current()) {
            case '{':
                parseTuple(parser);
                break;
            case '[':
                parseList(parser);
                break;
            case '"':
                type = GdbMiType.Const;
                data = parser.readCString();
                break;
        }
    }

    public boolean isValid() {
        return type != GdbMiType.Invalid;
    }

    public void reset() {
        name = null;
        data = null;
        type = GdbMiType.Invalid;
        if (!children.isEmpty())
            children = Collections.emptyList();
    }

    public String getName() {
        return name;
    }

    public String getData() {
        return data;
    }

    public GdbMiType getType() {
        return type;
    }

    private boolean isNameChar(char c) {
        return c != '=' && c != ':' && c != ']' && !Character.isSpaceChar(c);
    }

    private void parseTuple(@NotNull DebugOutputParser parser) {
        parser.advance();
        parseTupleHelper(parser);
    }

    private void parseList(@NotNull DebugOutputParser parser) {
        type = GdbMiType.List;
        parser.advance();
        parser.skipCommas();
        while (true) {
            if (parser.isCurrent(']')) {
                parser.advance();
                break;
            }
            var child = new GdbMi();
            child.parseResultOrValue(parser);
            if (!child.isValid())
                break;
            addChild(child);
            parser.skipCommas();
        }
    }

    private void parseTupleHelper(@NotNull DebugOutputParser parser) {
        type = GdbMiType.Tuple;
        parser.skipCommas();
        while (!parser.isAtEnd()) {
            if (parser.isCurrent('}')) {
                parser.advance();
                break;
            }
            var child = new GdbMi();
            child.parseResultOrValue(parser);
            if (!child.isValid()) {
                return;
            }
            addChild(child);
            parser.skipCommas();
        }
    }

    private void addChild(GdbMi child) {
        if (children.isEmpty())
            children = new LinkedList<>();
        children.add(child);
    }

    @Override
    public String toString() {
        return "{\"type\": \"" + type +
                "\", \"name\": \"" + name +
                "\", \"data\": \"" + data +
                "\", \"numChild\": \"" + children.size() +
                "}";
    }
}
