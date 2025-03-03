package ast;

import token.Token;

public class Identifier implements Expression {
    public Token token; 
    public String value;

    public Identifier(Token token, String value) {
        this.token = token;
        this.value = value;
    }

    @Override
    public void expressionNode() {
        // Required for Expression interface
    }

    @Override
    public String tokenLiteral() {
        return token.literal; // Direct access to token.literal
    }
}
