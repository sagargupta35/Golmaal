from sagar.my_token.token import Token, Constants

class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.position = 0
        self.read_position = 0
        self.ch = 0
    
    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def next_token(self) -> Token:
        con = Constants()
        tok = Token(con.EOF, '')

        match self.ch:
            case '=':
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
            case 0:
                tok = Token(con.EOF, '')
        
        self.read_char()
        return tok


def new_lexer(input: str) -> Lexer:
    l = Lexer(input= input)
    l.read_char()
    return l


        