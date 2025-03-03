package ast;

import token.Token;

public class ReturnStatement implements Statement {
    public Token token;
    public Expression returnValue; 

    public ReturnStatement(Token token, Expression returnValue) {
        this.token = token;
        this.returnValue = returnValue;
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
