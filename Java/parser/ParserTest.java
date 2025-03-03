// package parser;

// import ast.Program;
// import ast.Statement;
// import ast.LetStatement;
// import lexer.Lexer;
// import org.junit.jupiter.api.Test;
// import token.Token;

// import java.util.List;

// import static org.junit.jupiter.api.Assertions.*;

// class ParserTest {

//     @Test
//     void testLetStatements() {
//         String input = """
//                 let x = 5;
//                 let y = 10;
//                 let foobar = 838383;
//                 """;

//         Lexer lexer = new Lexer(input);
//         Parser parser = new Parser(lexer);
//         Program program = parser.parseProgram();

//         assertNotNull(program, "ParseProgram() returned null");

//         List<Statement> statements = program.getStatements();
//         assertEquals(3, statements.size(), "program.Statements does not contain 3 statements");

//         String[] expectedIdentifiers = {"x", "y", "foobar"};

//         for (int i = 0; i < expectedIdentifiers.length; i++) {
//             assertTrue(testLetStatement(statements.get(i), expectedIdentifiers[i]));
//         }
//     }

//     private boolean testLetStatement(Statement stmt, String name) {
//         if (!(stmt instanceof LetStatement letStmt)) {
//             fail("Statement is not a LetStatement. Got: " + stmt.getClass().getSimpleName());
//             return false;
//         }

//         if (!letStmt.token.type.equals("LET")) {
//             fail("TokenLiteral() is not 'let'. Got: " + letStmt.token.type);
//             return false;
//         }

//         if (!letStmt.name.value.equals(name)) {
//             fail("letStmt.Name.Value not '" + name + "'. Got: " + letStmt.name.value);
//             return false;
//         }

//         if (!letStmt.name.token.literal.equals(name)) {
//             fail("letStmt.Name.TokenLiteral() not '" + name + "'. Got: " + letStmt.name.token.literal);
//             return false;
//         }

//         return true;
//     }
// }

