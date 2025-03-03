package ast;

import token.Token;

public class LetStatement implements Statement {
    public Token token; // Stores the 'let' keyword
    public Identifier name; // Variable name
    public Expression value; // Assigned expression

    public LetStatement(Token token, Identifier name, Expression value) {
        this.token = token;
        this.name = name;
        this.value = value;
    }

    @Override
    public void statementNode() {
        //Baad me
    }

    @Override
    public String tokenLiteral() {
        return token.literal; 
    }
}
