package parser;

import lexer.Lexer;
import token.Token;

import java.util.ArrayList;
import java.util.List;

import ast.Identifier;
import ast.LetStatement;
import ast.Program;
import ast.ReturnStatement;
import ast.Statement;

public class Parser {
    private Lexer lexer;
    private Token curToken;
    private Token peekToken;
    private List<String> errors;  

    public Parser(Lexer lexer) {
        this.lexer = lexer;
        this.errors = new ArrayList<>();
        nextToken();
        nextToken();
    }

    private void nextToken() {
        curToken = peekToken;
        peekToken = lexer.nextToken();
    }

    public Program parseProgram() {
        Program program = new Program(new ArrayList<>());

        while (!curToken.type.equals("EOF")) {
            Statement stmt = parseStatement();
            if (stmt != null) {
                program.getStatements().add(stmt);
            }
            nextToken();
        }

        return program;
    }

    private Statement parseStatement() {
        switch (curToken.type) {
            case "LET":
                return parseLetStatement();
            case "RETURN":
                return parseReturnStatement();
            default:
                return null;
        }
    }

    private LetStatement parseLetStatement() {
        Token token = curToken; // Store LET token

        if (!expectPeek("IDENT")) {
            return null;
        }

        Identifier name = new Identifier(curToken, curToken.literal); // Variable name

        if (!expectPeek("=")) {
            return null;
        }

        // TODO: Skipping expressions for now (should later parse the expression)
        while (!curTokenIs(";")) {
            nextToken();
        }

        return new LetStatement(token, name, null); // Expression is null for now
    }

    private ReturnStatement parseReturnStatement() {
        Token token = curToken; 

        // TODO: Skipping expressions for now (should later parse the expression)
        while (!curTokenIs(";")) {
            nextToken();
        }

        return new ReturnStatement(token, null); // Expression is null for now
    }

    private boolean curTokenIs(String tokenType) {
        return curToken.type.equals(tokenType);
    }

    private boolean peekTokenIs(String tokenType) {
        return peekToken.type.equals(tokenType);
    }

    private boolean expectPeek(String tokenType) {
        if (peekTokenIs(tokenType)) {
            nextToken();
            return true;
        } else {
            peekError(tokenType);
            return false;
        }
    }

    private void peekError(String expectedType) {
        String msg = String.format("Expected next token to be %s, got %s instead", 
                                   expectedType, peekToken.type);
        errors.add(msg);
    }

    public List<String> getErrors() {
        return errors;
    }
    public static void main(String[] args) {
        String input = """
                        let x=10;
                        return 5;
                        return 10;
                        return 993322;
                        """;

        Lexer lexer = new Lexer(input);
        Parser parser = new Parser(lexer);
        Program program = parser.parseProgram();

        // Print errors if any
        if (!parser.getErrors().isEmpty()) {
            System.out.println("Parser errors:");
            for (String error : parser.getErrors()) {
                System.out.println(error);
            }
        } else {
            System.out.println("Parsing successful!");
        }
        // System.out.println(parser.getErrors());
    }
}
