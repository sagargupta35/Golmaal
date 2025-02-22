// // lexer/LexerTest.java
// package lexer;

// import org.junit.jupiter.api.Test;
// import token.Token;
// import token.TokenType;

// import static org.junit.jupiter.api.Assertions.*;

// public class LexerTest {

//     @Test
//     public void testNextToken() {
//         String input = "=+(){},;";

//         String[][] tests = {
//                 {TokenType.ASSIGN, "="},
//                 {TokenType.PLUS, "+"},
//                 {TokenType.LPAREN, "("},
//                 {TokenType.RPAREN, ")"},
//                 {TokenType.LBRACE, "{"},
//                 {TokenType.RBRACE, "}"},
//                 {TokenType.COMMA, ","},
//                 {TokenType.SEMICOLON, ";"},
//                 {TokenType.EOF, ""}
//         };

//         Lexer lexer = new Lexer(input);

//         for (int i = 0; i < tests.length; i++) {
//             Token tok = lexer.nextToken();
//             assertEquals(tests[i][0], tok.type, "tests[" + i + "] - TokenType wrong");
//             assertEquals(tests[i][1], tok.literal, "tests[" + i + "] - Literal wrong");
//         }
//     }
// }
