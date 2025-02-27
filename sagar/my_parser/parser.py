from sagar.lexer.Lexer import Lexer
from sagar.my_token.token import Token, Constants, TokenType
from sagar.my_ast.ast import Program, Statement, LetStatement, Identifier

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = lexer.next_token()
        self.peek_token: Token = lexer.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Program :
        program = Program()
        stmts = []

        while self.cur_token.token_type != Constants.EOF:
            stmt = self.parse_statement()
            if stmt:
                stmts.append(stmt)
            
            self.next_token()
        
        program.statements = stmts
        return program
    
    def parse_statement(self) -> Statement:
        match self.cur_token.token_type:
            case Constants.LET:
                letstmt =  self.parse_let_statement()
                return letstmt
            case _:
                return None
            
    def parse_let_statement(self) -> Statement:
        letstmt = LetStatement(token=self.cur_token, name = None, value = None)
        
        if self.peek_token.token_type != Constants.IDENT:
            print(f"Expected {Constants.IDENT}. But Found {self.peek_token.token_type}")
            return None
        
        self.next_token() # stands at iden
        name = Identifier(token = self.cur_token, value = self.cur_token.literal)
        letstmt.name = name
        
        if self.peek_token.token_type != Constants.ASSIGN:
            return None

        self.next_token() # stands at '='

        # Expression needs to be checked later
        while self.cur_token.token_type != Constants.SEMICOLON:
            self.next_token()

        return letstmt

        



        
        



        