package n.v.k.parser;

class DebugOutputParser {
    private final String _data;
    private int _index = 0;

    public DebugOutputParser(String data) {
        _data = data;
    }

    public char current() {
        return _data.charAt(_index);
    }

    public char lookAhead(int number) {
        return _data.charAt(_index + number);
    }

    public boolean isCurrent(char c) {
        return current() == c;
    }

    public boolean isAtEnd() {
        return _index >= _data.length();
    }

    public int remainingChars() {
        return _data.length() - _index;
    }

    public char readChar() {
        char c = current();
        advance();
        return c;
    }

    public void advance() {
        _index += 1;
    }

    public void advance(int n) {
        _index += n;
    }

    public interface CharValidator {
        boolean isValid(char c);
    }

    public String readString(CharValidator validator) {
        var sb = new StringBuilder(50);
        while (_index < _data.length() && validator.isValid(current())) {
            sb.append(readChar());
        }
        return sb.toString();
    }

    public String readCString() {
        if (isAtEnd())
            return "";

        if (current() != '"') {
            advance();
            return "";
        }

        advance();
        var sb = new StringBuilder(_data.length() - _index);
        while (_index < _data.length()) {
            if (isCurrent('"')) {
                advance();
                return sb.toString();
            }
            parseCharOrEscape(sb);
        }

        return "";
    }

    public void skipCommas() {
        while (_index < _data.length() && isCurrent(','))
            advance();
    }

    public void skipSpaces() {
        while (_index < _data.length() && Character.isWhitespace(current()))
            advance();
    }

    private void parseCharOrEscape(StringBuilder sb) {
        var sb1 = new StringBuilder(50);
        while (parseOctalEscaped(sb1)) {
        }
        while (parseHexEscaped(sb1)) {
        }
        if (sb1.length() > 0) {
            sb.append(sb1);
        } else if (isCurrent('\\')) {
            advance();
            parseSimpleEscape(sb);
        } else {
            sb.append(readChar());
        }
    }

    private boolean parseOctalEscaped(StringBuilder sb) {
        if (remainingChars() < 4)
            return false;
        if (!isCurrent('\\'))
            return false;

        char c1 = lookAhead(1);
        char c2 = lookAhead(2);
        char c3 = lookAhead(3);
        if (!Character.isDigit(c1) || !Character.isDigit(c2) || !Character.isDigit(c3))
            return false;

        int zero = Character.digit('0', 10);
        sb.append(Character.forDigit((Character.digit(c1, 10) - zero) * 64
                + (Character.digit(c2, 10) - zero) * 8
                + Character.digit(c3, 10) - zero, 10));
        advance(4);
        return true;
    }

    private boolean parseHexEscaped(StringBuilder sb) {
        if (remainingChars() < 4)
            return false;
        if (!isCurrent('\\'))
            return false;
        if (lookAhead(1) != 'x')
            return false;

        int c1 = Character.digit(lookAhead(2), 16);
        int c2 = Character.digit(lookAhead(3), 16);
        if (c1 < 0 || c1 > 15 || c2 < 0 || c2 > 15)
            return false;

        sb.append(Character.forDigit(c1 * 16 + c2, 16));
        advance(4);
        return true;
    }

    private void parseSimpleEscape(StringBuilder sb) {
        char current = current();
        advance();

        switch (current) {
            //case 'a': sb.append('\a'); break;
            case 'b':
                sb.append('\b');
                break;
            case 'f':
                sb.append('\f');
                break;
            case 'n':
                sb.append('\n');
                break;
            case 'r':
                sb.append('\r');
                break;
            case 't':
                sb.append('\t');
                break;
            //case 'v': sb.append('\v'); break;
            case '"':
                sb.append('"');
                break;
            case '\'':
                sb.append('\'');
                break;
            case '\\':
                sb.append('\\');
                break;
        }
    }
}
