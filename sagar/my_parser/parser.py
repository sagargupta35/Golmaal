from sagar.lexer.Lexer import Lexer
from sagar.my_token.token import Token, Constants, TokenType
from sagar.my_ast.ast import *
from typing import Callable

prefix_parsing_fn = Callable[[], Expression]
infix_parsing_fn = Callable[[Expression], Expression]


LOWEST = 1
EQUALS = 2
LESSGREATER = 3
SUM = 4
PRODUCT = 5
PREFIX = 6
CALL = 7

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = lexer.next_token()
        self.peek_token: Token = lexer.next_token()
        self.errors: list[str] = []
        self.prefix_parsing_fns: dict[TokenType, prefix_parsing_fn] = {}
        self.infix_parsing_fns: dict[TokenType, infix_parsing_fn] = {}
        self.__register_paring_fns()

    def __register_paring_fns(self):
        self.prefix_parsing_fns[Constants.IDENT] = self.parse_identifier
        self.prefix_parsing_fns[Constants.INT] = self.parse_integer_literal
        self.prefix_parsing_fns[Constants.BANG] = self.parse_prefix_expression
        self.prefix_parsing_fns[Constants.MINUS] = self.parse_prefix_expression

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
            case Constants.RETURN:
                rt_stmt = self.parse_return_statement()
                return rt_stmt
            case _:
                exp_stmt = self.parse_expression_statement()
                return exp_stmt
            
    def parse_let_statement(self) -> Statement:
        letstmt = LetStatement(token=self.cur_token, name = None, value = None)
        
        if not self.expect_peek(Constants.IDENT):
            print(f"Expected {Constants.IDENT}. But Found {self.peek_token.token_type}")
            return None
        
        # stands at iden
        name = Identifier(token = self.cur_token, value = self.cur_token.literal)
        letstmt.name = name
        
        if not self.expect_peek(Constants.ASSIGN):
            return None

        # stands at '='

        # Expression needs to be checked later
        while self.cur_token.token_type != Constants.SEMICOLON:
            self.next_token()

        return letstmt
    
    def parse_return_statement(self):
        rt_stmt = ReturnStatement(token = self.cur_token, value = None)

        self.next_token() # stands at the start of the expression
        #Expression needs to be checked later
        while self.cur_token.token_type != ';':
            self.next_token()
        return rt_stmt

    def expect_peek(self, token_type: TokenType) -> bool:
        if self.peek_token.token_type == token_type:
            self.next_token()
            return True
        else:
            self.peek_error(token_type)
            return False
    
    def peek_error(self, token_type: TokenType):
        msg = f"Expected '{token_type}'. But found '{self.peek_token.token_type}'"
        self.errors.append(msg)


    def parse_expression_statement(self) -> Statement:
        exp_stmt = ExpressionStatement(token = self.cur_token, expression = None)

        exp_stmt.expression = self.parse_expression(LOWEST)

        if self.peek_token.token_type == Constants.SEMICOLON:
            self.next_token()
        
        return exp_stmt
    
    def parse_expression(self, precedence: int) -> Expression:
        prefix = self.prefix_parsing_fns.get(self.cur_token.token_type)

        if prefix == None:
            self.errors.append(f"no prefix parsing function found for {self.cur_token.token_type}")
            return None
        
        left_exp = prefix()
        return left_exp
    
    def parse_identifier(self) -> Expression:
        return Identifier(token = self.cur_token, value = self.cur_token.literal)
    
    def parse_integer_literal(self) -> Expression:
        try:
            return IntegerLiteral(token= self.cur_token, value=int(self.cur_token.literal))
        except (ValueError, TypeError):
            return None
        
    def parse_prefix_expression(self) -> Expression:
        expression = PrefixExpression(token= self.cur_token, operator=self.cur_token.literal, right= None)
        self.next_token() # consume the operator
        expression.right = self.parse_expression(precedence=PREFIX)
        return expression







        



        
        



        