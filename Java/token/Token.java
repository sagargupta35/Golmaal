// token/Token.java
package token;

public class Token {
    public String type;
    public String literal;

    public Token(String type, String literal) {
        this.type = type;
        this.literal = literal;
    }
}
