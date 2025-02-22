import unittest
from mylexer.lexer import Lexer
from mytoken.tokentype import TokenType

class TestLexer(unittest.TestCase):
    def test_next_token(self):
        input_text = "=+(){}*;"

        tests = [
            (TokenType.ASSIGN, "="),
            (TokenType.PLUS, "+"),
            (TokenType.LPAREN, "("),
            (TokenType.RPAREN, ")"),
            (TokenType.LBRACE, "{"),
            (TokenType.RBRACE, "}"),
            (TokenType.COMMA, ","),
            (TokenType.SEMICOLON, ";"),
            (TokenType.EOF, "")
        ]

        lexer = Lexer(input_text)

        for i, (expected_type, expected_literal) in enumerate(tests):
            tok = lexer.next_token()
            self.assertEqual(tok.type, expected_type, f"Test[{i}] - TokenType wrong. Expected={expected_type}, Got={tok.type}")
            self.assertEqual(tok.literal, expected_literal, f"Test[{i}] - Literal wrong. Expected={expected_literal}, Got={tok.literal}")

if __name__ == '__main__':
    unittest.main()
