package ast;

import java.util.List;

public class Program implements Node {
    private List<Statement> statements;

    public Program(List<Statement> statements) {
        this.statements = statements;
    }

    public List<Statement> getStatements() {
        return statements;
    }

    @Override
    public String tokenLiteral() {
        return (statements != null && !statements.isEmpty()) 
               ? statements.get(0).tokenLiteral() 
               : "";
    }
}
