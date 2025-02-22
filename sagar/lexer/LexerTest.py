import unittest
from sagar.lexer import Lexer
from sagar.my_token.token import Constants

class TestNextToken(unittest.TestCase):

    def test_next_token(self):
        input = '''
            let five = 5;
            let ten = 10;
            let add = fn(x, y){
                x + y;
            }
            let result = add(five, ten);
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
            (con.EOF, ""),
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



            

