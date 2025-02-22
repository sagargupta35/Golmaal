# lexer/lexer.py
from mytoken.token import Token
from mytoken.tokentype import TokenType

class Lexer:
    def __init__(self, input_str):
        self.input = input_str
        self.position = 0
        self.read_position = 0
        self.ch = ''
        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = '\0'  # EOF equivalent
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def next_token(self):
        token_map = {
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ',': TokenType.COMMA,
            ';': TokenType.SEMICOLON,
            '\0': TokenType.EOF
        }

        tok_type = token_map.get(self.ch, TokenType.ILLEGAL)
        tok = Token(tok_type, self.ch if self.ch != '\0' else '')

        self.read_char()
        return tok
