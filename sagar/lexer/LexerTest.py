import unittest
from sagar.lexer import Lexer
from sagar.my_token.token import Constants

class TestNextToken(unittest.TestCase):

    def test_next_token(self):
        input = '''
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
            "foobar"
            "foo bar"
            [1, 2];
        '''
        con = Constants()

        tokens = [
            (con.LET, "let"),
            (con.IDENT, "five"),
            (con.ASSIGN, "="),
            (con.INT, "5"),
            (con.SEMICOLON, ";"),

            (con.LET, "let"),
            (con.IDENT, "ten"),
            (con.ASSIGN, "="),
            (con.INT, "10"),
            (con.SEMICOLON, ";"),

            (con.LET, "let"),
            (con.IDENT, "add"),
            (con.ASSIGN, "="),
            (con.FUNCTION, "fn"),
            (con.LPAREN, "("),
            (con.IDENT, "x"),
            (con.COMMA, ","),
            (con.IDENT, "y"),
            (con.RPAREN, ")"),
            (con.LBRACE, "{"),

            (con.IDENT, "x"),
            (con.PLUS, "+"),
            (con.IDENT, "y"),
            (con.SEMICOLON, ";"),

            (con.RBRACE, "}"),
            (con.SEMICOLON, ";"),

            (con.LET, "let"),
            (con.IDENT, "result"),
            (con.ASSIGN, "="),
            (con.IDENT, "add"),
            (con.LPAREN, "("),
            (con.IDENT, "five"),
            (con.COMMA, ","),
            (con.IDENT, "ten"),
            (con.RPAREN, ")"),
            (con.SEMICOLON, ";"),

            (con.BANG, "!"),
            (con.MINUS, "-"),
            (con.SLASH, "/"),
            (con.ASTERISK, "*"),
            (con.INT, "5"),
            (con.SEMICOLON, ";"),

            (con.INT, "5"),
            (con.LT, "<"),
            (con.INT, "10"),
            (con.GT, ">"),
            (con.INT, "5"),
            (con.SEMICOLON, ";"),

            (con.IF, "if"),
            (con.LPAREN, "("),
            (con.INT, "5"),
            (con.LT, "<"),
            (con.INT, "10"),
            (con.RPAREN, ")"),
            (con.LBRACE, "{"),

            (con.RETURN, "return"),
            (con.TRUE, "true"),
            (con.SEMICOLON, ";"),

            (con.RBRACE, "}"),
            (con.ELSE, "else"),
            (con.LBRACE, "{"),

            (con.RETURN, "return"),
            (con.FALSE, "false"),
            (con.SEMICOLON, ";"),

            (con.RBRACE, "}"),

            (con.INT, "10"),
            (con.EQ, "=="),
            (con.INT, "10"),
            (con.SEMICOLON, ";"),

            (con.INT, "10"),
            (con.NOT_EQ, "!="),
            (con.INT, "9"),
            (con.SEMICOLON, ";"),

            (con.STRING, 'foobar'),
            (con.STRING, 'foo bar'),
            (con.LBRACKET, '['),
            (con.INT, '1'),
            (con.COMMA, ','),
            (con.INT, '2'),
            (con.RBRACKET, ']'),
            (con.SEMICOLON, ';'),
            (con.EOF, '')
        ]


        l = Lexer.new_lexer(input)

        for i, (exp_type, exp_literal) in enumerate(tokens):
            tok = l.next_token()
            self.assertEqual(
                tok.token_type,
                exp_type,
                f"Failed to match token type of token {i}. Expected {exp_type}. But found {tok.token_type}"
            )

            self.assertEqual(
                tok.literal,
                exp_literal,
                f"Failed to match token literal of token {i}. Expected {exp_literal}. But found {tok.literal}"
            )


if __name__ == "__main__":
    unittest.main()



            

