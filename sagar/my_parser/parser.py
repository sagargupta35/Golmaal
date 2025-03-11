from sagar.lexer.Lexer import Lexer, is_letter_or_digit
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

precedences: dict[TokenType, int] = {
    Constants.EQ: EQUALS,
    Constants.NOT_EQ: EQUALS,
    Constants.LT: LESSGREATER,
    Constants.GT: LESSGREATER,
    Constants.PLUS: SUM,
    Constants.MINUS: SUM,
    Constants.SLASH: PRODUCT,
    Constants.ASTERISK: PRODUCT,
    Constants.LPAREN: CALL
}

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
        self.prefix_parsing_fns[Constants.TRUE] = self.parse_boolean_expression
        self.prefix_parsing_fns[Constants.FALSE] = self.parse_boolean_expression
        self.prefix_parsing_fns[Constants.LPAREN] = self.parse_grouped_expression
        self.prefix_parsing_fns[Constants.IF] = self.parse_if_expression
        self.prefix_parsing_fns[Constants.FUNCTION] = self.parse_function_literal

        infix_ops = ['+', '-', '==', '!=', '/', '*', '<', '>']
        for infix_op in infix_ops:
            self.infix_parsing_fns[infix_op] = self.parse_infix_expression
        
        self.infix_parsing_fns[Constants.LPAREN] = self.parse_lparen_infix

    def peek_precedence(self):
        return precedences.get(self.peek_token.token_type, LOWEST)
    
    def cur_precedence(self):
        return precedences.get(self.cur_token.token_type, LOWEST)

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
            
    def parse_let_statement(self) -> LetStatement:
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
    
    def parse_return_statement(self) -> ReturnStatement:
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

        while self.peek_token != Constants.SEMICOLON and self.peek_precedence() > precedence:
            infix = self.infix_parsing_fns[self.peek_token.token_type]

            if infix == None:
                return left_exp
            
            self.next_token()

            left_exp = infix(left_exp)
        
        return left_exp
    
    def parse_infix_expression(self, left: Expression) -> Expression:
        inf_exp = InfixExpression(token=self.cur_token, left= left, operator=self.cur_token.literal, right= None)
        cur_precedence = self.cur_precedence()
        self.next_token()
        right = self.parse_expression(precedence=cur_precedence)
        inf_exp.right = right
        return inf_exp

    
    def parse_identifier(self) -> Expression:
        if not self.ensure_identifier_naming_convention(self.cur_token.literal):
            self.errors.append(f'{self.cur_token.literal} does not follow proper naming convention of an identifier')
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
    
    def parse_boolean_expression(self) -> Expression:
        bool_exp = Boolean(token = self.cur_token, value = self.cur_token.token_type == Constants.TRUE)
        return bool_exp
    
    def parse_grouped_expression(self) -> Expression:
        self.next_token()
        exp = self.parse_expression(LOWEST)
        if not self.expect_peek(Constants.RPAREN):
            return None
        return exp
    
    def parse_if_expression(self) -> IfExpression:
        if_exp = IfExpression(token = self.cur_token, condition=None, consequence=None, alternative=None)
        self.next_token() 
        
        #stands at (
        if_exp.condition = self.parse_grouped_expression() # after this token is at )
        
        if not self.expect_peek(Constants.LBRACE):
            return None

        consequence: BlockStatement = self.parse_block_statement()
        if_exp.consequence = consequence

        if self.peek_token.token_type == Constants.ELSE:
            self.next_token() # stands at else
            if not self.expect_peek(Constants.LBRACE):
                return None
            if_exp.alternative = self.parse_block_statement()

        return if_exp
    

    def parse_block_statement(self) -> BlockStatement:
        block_stmt = BlockStatement(token=self.cur_token)
        self.next_token() # token is at {
        
        while self.cur_token.token_type != Constants.RBRACE and self.cur_token.token_type != Constants.EOF:
            stmt = self.parse_statement()
            if stmt:
                block_stmt.statements.append(stmt)
            self.next_token() # move to the next statement (might be standing at semicolon or not)

        if self.cur_token.token_type != Constants.RBRACE:
            self.errors.append(f'Expected {Constants.RBRACE} at the end of block statment. But it is {self.cur_token}')
            return None
        
        return block_stmt

    def parse_function_literal(self) -> FunctionLiteral:
        fn_lit = FunctionLiteral(token = self.cur_token)

        params: list[Identifier] = []
        self.expect_peek(Constants.LPAREN) # stands at Lparen

        while self.cur_token.token_type not in  [Constants.EOF, Constants.RPAREN]:
            self.next_token()
            #takes care for zero params or , after all params followed by ) while you are expecting an identifier
            if self.cur_token.token_type in [Constants.RPAREN, Constants.EOF]: 
                break
            params.append(self.parse_identifier())
            self.next_token() # move to next , or )
            if self.cur_token.token_type not in [Constants.COMMA, Constants.RPAREN]:
                self.errors.append(f'Expected ")" or "," after parameter. Not {self.cur_token.token_type}')
                return None
            
        if self.cur_token.token_type != Constants.RPAREN:
            self.errors.append("Expected ) after declaring parameters")
            return None

        fn_lit.parameters = params
        if not self.expect_peek(Constants.LBRACE):
            return None

        fn_lit.body = self.parse_block_statement()

        return fn_lit

    def parse_lparen_infix(self, left: Expression) -> CallExpression:
        call_exp = CallExpression(token=self.cur_token, function=left)
        
        args = []
        
        while self.cur_token.token_type not in [Constants.RPAREN, Constants.EOF]:
            self.next_token()
            if self.cur_token.token_type in [Constants.RPAREN, Constants.EOF]: 
                break
            args.append(self.parse_expression(LOWEST))
            if self.peek_token.token_type not in [Constants.RPAREN, Constants.COMMA]:
                self.errors.append(f'Expected , or ) after each argument in the CallExpression')
                return None
            self.next_token()
        
        if self.cur_token.token_type != Constants.RPAREN:
            return None
        
        call_exp.arguments = args
        return call_exp

    def ensure_identifier_naming_convention(self, name) -> False:
        if type(name) is not str:
            return False
        if len(name) == 0:
            return False
        if (name[0] < 'a' or name[0] > 'z') and (name[0] < 'A' or name[0] > 'Z'):
            return False
        for c in name:
            if not is_letter_or_digit(c):
                return False
        return True

    


    




  