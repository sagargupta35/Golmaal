from sagar.my_token import token
from sagar.my_token.token import Token, Constants


class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.position = -1
        self.read_position = 0
        self.ch = 0
    
    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def peek_char(self):
        if self.read_position >= len(self.input):
            return 0
        else:
            return self.input[self.read_position]

    def read_word(self) -> str:
        pos = self.position
        while is_letter_or_digit(self.peek_char()):
            self.read_char()
        return self.input[pos:self.read_position]
    
    def read_two_char(self) -> Token:
        ch = self.ch
        self.read_char()
        two_char_tok_type = token.get_two_char_type(ch+self.ch)
        return Token(two_char_tok_type, ch+self.ch)

    def next_token(self) -> Token:
        con = Constants()
        tok = Token(con.EOF, '')
        
        self.skip_whitespace()

        match self.ch:
            case '=':
                if self.peek_char() == '=':
                    tok = self.read_two_char()
                else:
                    tok = Token(con.ASSIGN, '=')
            case ';':
                tok = Token(con.SEMICOLON, ';')
            case '(':
                tok = Token(con.LPAREN, '(')
            case ')':
                tok = Token(con.RPAREN, ')')
            case ',':
                tok = Token(con.COMMA, ',')
            case '+':
                tok = Token(con.PLUS, '+')
            case '{':
                tok = Token(con.LBRACE, '{')
            case '}':
                tok = Token(con.RBRACE, '}')
            case '!':
                if self.peek_char() == '=':
                    tok = self.read_two_char()
                else:
                    tok = Token(con.BANG, '!')
            case '-':
                tok = Token(con.MINUS, '-')
            case '/':
                tok = Token(con.SLASH, '/')
            case '<':
                tok = Token(con.LT, '<')
            case '>':
                tok = Token(con.GT, '>')
            case '*':
                tok = Token(con.ASTERISK, '*')
            case 0:
                tok = Token(con.EOF, '')
            case _:
                if is_letter_or_digit(self.ch):
                    word = self.read_word()
                    if is_number(word):
                        tok = Token(con.INT, word)
                    elif is_digit(word[0]):
                        tok = Token(con.ILLEGAL, word)
                    else:
                        tok = Token(token.get_ident_type(word), word)
                else:
                    tok = Token(con.ILLEGAL, self.ch)

        self.read_char()
        return tok

    
    def skip_whitespace(self):
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.read_char()


def new_lexer(input: str) -> Lexer:
    l = Lexer(input= input)
    l.read_char()
    return l

def is_letter_or_digit(ch: str) -> bool:
    return (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') or ch == '_' or is_digit(ch)

def is_digit(ch: str) -> bool:
    return ch >= '0' and ch <= '9'

def is_number(ch: str) -> bool:
    for c in ch:
        if not is_digit(c):
            return False
    return True

