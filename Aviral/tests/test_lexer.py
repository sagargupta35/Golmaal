import unittest
from mylexer.lexer import Lexer
from mytoken.tokentype import TokenType

class TestLexer(unittest.TestCase):
    def test_next_token(self):
        input_text = "=+(){}*;"
        input_text = '''
            let five = 5;
            let ten = 10;
            let add = fn(x, y) {
            x + y;
            };
            let result = add(five, ten);
            !-/*5;
            5 < 10 > 5;
            if (5 < 10) {
            return true;
            } else {
            return false;
            }
            10 == 10;
            10 != 9;
        '''
        tests = [
            (TokenType.LET, "let"),
            (TokenType.IDENT, "five"),
            (TokenType.ASSIGN, "="),
            (TokenType.INT, "5"),
            (TokenType.SEMICOLON, ";"),

            (TokenType.LET, "let"),
            (TokenType.IDENT, "ten"),
            (TokenType.ASSIGN, "="),
            (TokenType.INT, "10"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.LET, "let"),
            (TokenType.IDENT, "add"),
            (TokenType.ASSIGN, "="),
            (TokenType.FUNCTION, "fn"),
            (TokenType.LPAREN, "("),
            (TokenType.IDENT, "x"),
            (TokenType.COMMA, ","),
            (TokenType.IDENT, "y"),
            (TokenType.RPAREN, ")"),
            (TokenType.LBRACE, "{"),

            (TokenType.IDENT, "x"),
            (TokenType.PLUS, "+"),
            (TokenType.IDENT, "y"),
            (TokenType.SEMICOLON, ";"),

            (TokenType.RBRACE, "}"),
            (TokenType.SEMICOLON, ";"),

            (TokenType.LET, "let"),
            (TokenType.IDENT, "result"),
            (TokenType.ASSIGN, "="),
            (TokenType.IDENT, "add"),
            (TokenType.LPAREN, "("),
            (TokenType.IDENT, "five"),
            (TokenType.COMMA, ","),
            (TokenType.IDENT, "ten"),
            (TokenType.RPAREN, ")"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.BANG, "!"),
            (TokenType.MINUS, "-"),
            (TokenType.SLASH, "/"),
            (TokenType.ASTERISK, "*"),
            (TokenType.INT, "5"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.INT, "5"),
            (TokenType.LT, "<"),
            (TokenType.INT, "10"),
            (TokenType.GT, ">"),
            (TokenType.INT, "5"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.IF, "if"),
            (TokenType.LPAREN, "("),
            (TokenType.INT, "5"),
            (TokenType.LT, "<"),
            (TokenType.INT, "10"),
            (TokenType.RPAREN, ")"),
            (TokenType.LBRACE, "{"),
            (TokenType.RETURN, "return"),
            (TokenType.TRUE, "true"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.RBRACE, "}"),
            (TokenType.ELSE, "else"),
            (TokenType.LBRACE, "{"),
            (TokenType.RETURN, "return"),
            (TokenType.FALSE, "false"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.RBRACE, "}"),
            (TokenType.INT, "10"),
            (TokenType.EQ, "=="),
            (TokenType.INT, "10"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.INT, "10"),
            (TokenType.NOT_EQ, "!="),
            (TokenType.INT, "9"),
            (TokenType.SEMICOLON, ";")
        ]
        lexer = Lexer(input_text)

        for i, (expected_type, expected_literal) in enumerate(tests):
            tok = lexer.next_token()
            self.assertEqual(tok.type, expected_type, f"Test[{i}] - TokenType wrong. Expected={expected_type}, Got={tok.type}")
            self.assertEqual(tok.literal, expected_literal, f"Test[{i}] - Literal wrong. Expected={expected_literal}, Got={tok.literal}")

if __name__ == '__main__':
    unittest.main()
