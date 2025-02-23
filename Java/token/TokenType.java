// token/TokenType.java
package token;

import java.util.HashMap;
import java.util.Map;

public class TokenType {
    public static final String ILLEGAL = "ILLEGAL";
    public static final String EOF = "EOF";

    public static final String IDENT = "IDENT";
    public static final String INT = "INT";

    public static final String ASSIGN = "=";
    public static final String PLUS = "+";

    public static final String COMMA = ",";
    public static final String SEMICOLON = ";";
    public static final String LPAREN = "(";
    public static final String RPAREN = ")";
    public static final String LBRACE = "{";
    public static final String RBRACE = "}";
    public static final String FUNCTION = "FUNCTION";
    public static final String LET = "LET";
    private static final Map<String, String> keywords = new HashMap<>();
    static {
        keywords.put("let", LET);
        keywords.put("fn", FUNCTION);
    }
    public static String getIdentType(String s){
        return keywords.getOrDefault(s, IDENT);
    }
}
