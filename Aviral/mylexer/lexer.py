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

    def peek_char(self):
        if self.read_position >= len(self.input):
            return '\0'
        return self.input[self.read_position]

    def skip_whitespace(self):
        while self.ch in (' ', '\n', '\r', '\t'):
            self.read_char()

    def is_letter_or_digit(self, ch):
        return ch.isalpha() or ch.isdigit() or ch == '_'

    def is_digit(self, ch):
        return ch.isdigit()

    def read_word(self):
        pos = self.position
        while self.is_letter_or_digit(self.ch):
            self.read_char()
        return self.input[pos:self.position]

    def is_number(self, s):
        return s.isdigit()

    def next_token(self):
        self.skip_whitespace()

        if self.ch == '=':
            if self.peek_char() == '=':
                prev_ch = self.ch
                self.read_char()
                tok = Token(TokenType.EQ, prev_ch + self.ch)
            else:
                tok = Token(TokenType.ASSIGN, self.ch)

        elif self.ch == '!':
            if self.peek_char() == '=':
                prev_ch = self.ch
                self.read_char()
                tok = Token(TokenType.NOT_EQ, prev_ch + self.ch)
            else:
                tok = Token(TokenType.BANG, self.ch)

        elif self.ch in '+-*/<>(),;{}':
            token_map = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.ASTERISK,
                '/': TokenType.SLASH,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON
            }
            tok = Token(token_map[self.ch], self.ch)

        elif self.ch == '\0':
            tok = Token(TokenType.EOF, '')

        elif self.is_letter_or_digit(self.ch):
            word = self.read_word()
            if self.is_number(word):
                tok = Token(TokenType.INT, word)
            elif word[0].isdigit():
                tok = Token(TokenType.ILLEGAL, word)
            else:
                tok = Token(TokenType.get_ident_type(word), word)
            return tok  

        else:
            tok = Token(TokenType.ILLEGAL, self.ch)

        self.read_char()
        return tok