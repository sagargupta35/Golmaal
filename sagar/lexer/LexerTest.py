import unittest
from sagar.lexer import Lexer
from sagar.my_token.token import Constants

class TestNextToken(unittest.TestCase):

    def test_next_token(self):
        input = "=+(){},;"
        con = Constants()

        tokens = [
            (con.ASSIGN, "="),
            (con.PLUS, "+"),
            (con.LPAREN, "("),
            (con.RPAREN, ")"),
            (con.LBRACE, "{"),
            (con.RBRACE, "}"),
            (con.COMMA, ","),
            (con.SEMICOLON, ";"),
            (con.EOF, "")
        ]

        l = Lexer.new_lexer(input)

        for i, (exp_type, exp_literal) in enumerate(tokens):
            tok = l.next_token()

            self.assertEqual(
                tok.token_type,
                exp_type,
                f"Failed to match token type at index ${i}.\
                  Expected ${exp_type}. But found ${tok.token_type}"
            )

            self.assertEqual(
                tok.literal,
                exp_literal,
                f"Failed to match token literal at index ${i}.\
                Expected ${exp_literal}. But found ${tok.literal}"
            )


if __name__ == "__main__":
    unittest.main()



            

