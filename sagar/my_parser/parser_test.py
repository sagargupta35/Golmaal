import unittest
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_ast.ast import *
from sagar.my_token.token import Token, Constants


class TestParser(unittest.TestCase):
    
    def test_let_statement(self):
        inp = '''
            jaadu five = 5;
            jaadu t = true;
            jaadu foobar = y;
        '''

        l = new_lexer(inp)
        p = Parser(lexer= l)

        identifiers = [('five', 5), ('t', True), ('foobar', 'y')]

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(program != None, f"Unable to parse program. Parser returned None")
        self.assertTrue(len(program.statements) == 3, f"Expected 3 statements. But found {len(program.statements)}")

        for (iden, exp), stmt in zip(identifiers, program.statements):
            self.validate_let_statement(stmt, iden, exp)

    def validate_let_statement(self, stmt: Statement, iden: str, expected):
        self.assertTrue(stmt.token_literal() == 'jaadu', f"Expected jaadu as token literal for stmt. But found {stmt.token_literal()}")
        self.assertTrue(isinstance(stmt, LetStatement), f"stmt is not instance of LetStatement. It is a {type(stmt)}")
        letstmt: LetStatement = stmt
        self.assertTrue(letstmt.name.token_literal() == iden, f"letstmt.name.token_literal() is not {iden}. Found {letstmt.name.token_literal()}")
        self.assertTrue(letstmt.name.value == iden, f"letstmt.name.value is not {iden}. Found {letstmt.name.value}")
        self.validate_literal_expression(letstmt.value, expected)


    def test_return_statement(self):
        inp = '''
            ye_lo 10;
            ye_lo 5;
            ye_lo 342934923;
        '''

        l = new_lexer(inp)
        p = Parser(lexer=l)

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(program != None, "p.parse_program() returned null.")
        self.assertTrue(len(program.statements) == 3, f"Expected 3 statements. But found {len(program.statements)} statements")
        
        for i, stmt in enumerate(program.statements):
            self.assertTrue(stmt.token_literal() == 'ye_lo', f"Expected return as token_literal. But found {stmt.token_literal()}")
            self.assertTrue(isinstance(stmt, ReturnStatement), f"stmt {i} is not an instance of ReturnStatment")


    def test_identifier_expression(self):
        inp = 'foobar;'

        l = new_lexer(inp)
        p = Parser(lexer=l)

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(program != None, "p.parse_program() returned null.")
        self.assertTrue(len(program.statements) == 1, f"Expected 1 statement. But found {len(program.statements)} statements")

        stmt = program.statements[0]
        self.assertTrue(isinstance(stmt, ExpressionStatement), f"stmt is not an instance of Statement. It is a {type(stmt)}")

        exp_stmt: ExpressionStatement = stmt
        self.validate_identifier_expression(exp_stmt.expression, value='foobar')

    def validate_identifier_expression(self, iden: Expression, value: str):
        self.assertTrue(isinstance(iden, Identifier), f"exp_stmt.expression is not an instance of Identifier. It is a {type(iden)}")
        self.assertTrue(iden.value == value, f"iden.value is not '{value}'. Found {iden.value}")
        self.assertTrue(iden.token_literal() == value, f"iden.token_literal() is not '{value}'. Found {iden.token_literal()}")

    
    def test_integer_literals(self):
        inp = '''
            5;
            9379;
        '''

        values = [5, 9379]

        l = new_lexer(input=inp)
        p = Parser(l)

        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertTrue(program != None, "p.parse_program() returned None")
        self.assertTrue(len(program.statements) == 2, f"Expected 2 statments. But found {len(program.statements)}")

        for i, stmt in enumerate(program.statements):
            self.assertTrue(isinstance(stmt, ExpressionStatement), f"stmt {i} is not an Expression statment. Its a {type(stmt)}")
            exp_stmt: ExpressionStatement = stmt
            self.validate_integer_literal(right=exp_stmt.expression, int_val=values[i])

    def validate_literal_expression(self, exp: Expression, expected):
        if type(expected) is bool:
            self.validate_boolean_expression(exp, expected)
        elif type(expected) is str :
            self.validate_identifier_expression(exp, expected)
        elif type(expected) is int:
            self.validate_integer_literal(exp, expected)
        else:
            self.fail(f"Invalid type of expected = {type(expected)}")

    def test_prefix_expression(self):
        prefix_exps = [("!5", "!", 5), ("-1", "-", 1), ("!true", "!", True), ("!false", "!", False)]

        for inp, op, val in prefix_exps:
            l = new_lexer(input=inp)
            p = Parser(lexer= l)

            program = p.parse_program()
            self.check_parse_errors(p)

            self.assertTrue(len(program.statements) == 1, f"Length of program.statments != 1. Its {len(program.statements)}")
            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, ExpressionStatement), f"stmt is not an instance of ExpressionStatement. Its a {type(stmt)}")
            exp_stmt: ExpressionStatement = stmt
            
            self.assertTrue(isinstance(exp_stmt.expression, PrefixExpression), f"exp_stmt.expression is not an instance of PrefixExpression. Its a {type(exp_stmt.expression)}")
            exp: PrefixExpression = exp_stmt.expression

            self.assertTrue(exp.operator == op, f"exp.operator != {op}. Its {exp.operator}")
            self.validate_literal_expression(exp.right, val)

    def test_infix_expression(self):
        infix_tests = [
            ("5 + 5;", 5, "+", 5),
            ("5 - 5;", 5, "-", 5),
            ("5 * 5;", 5, "*", 5),
            ("5 / 5;", 5, "/", 5),
            ("5 > 5;", 5, ">", 5),
            ("5 < 5;", 5, "<", 5),
            ("5 == 5;", 5, "==", 5),
            ("5 != 5;", 5, "!=", 5),
        ]

        for i, tt in enumerate(infix_tests):
            inp, left, op, right = tt
            l = new_lexer(inp)
            p = Parser(l)

            program = p.parse_program()
            self.check_parse_errors(p)
            self.assertTrue(len(program.statements) == 1, f"len(program.statement) = {len(program.statements)} != 1")

            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, ExpressionStatement), f"stmt {i} is not an ExpressionStatement. Its a {type(stmt)}")
            exp_stmt: ExpressionStatement = stmt

            self.assertTrue(isinstance(exp_stmt.expression, InfixExpression), f"exp_stmt {i} is not an InfixExpression. Its a {type(stmt)}")
            inf_stmt: InfixExpression = exp_stmt.expression

            self.validate_integer_literal(right=inf_stmt.left, int_val=left)
            self.assertTrue(inf_stmt.operator == op, f"inf_stmt{i}.operator == {inf_stmt.operator} != {op}")
            self.validate_integer_literal(right= inf_stmt.right, int_val=right)

    def validate_infix_expression(self, exp: Expression, left, operator: str, right):
        self.assertTrue(isinstance(exp, InfixExpression), f"type(exp) = {type(exp)} != InfixExpression")
        op_exp: InfixExpression = exp
        self.validate_literal_expression(op_exp.left, left)
        self.assertTrue(op_exp.operator == operator, f"op_exp.operator = {op_exp.operator} != {operator}")
        self.validate_literal_expression(op_exp.right, right)

    def test_operator_precedence(self):
        tests = [( "-a * b", "((-a) * b)"), ("!-a", "(!(-a))"), ("a + b + c", "((a + b) + c)"),\
                ("a + b- c", "((a + b) - c)"), ("a * b * c", "((a * b) * c)"), ("a * b / c", "((a * b) / c)"),\
                ("a + b / c", "(a + (b / c))"), ("a + b * c + d / e- f", "(((a + (b * c)) + (d / e)) - f)"),\
                ("3 + 4;-5 * 5", "(3 + 4)((-5) * 5)"), ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),\
                ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),\
                ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),\
                ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"), ("true", "True"),\
                ("false", "False"), ("3 > 5 == False", "((3 > 5) == False)"), ("3 < 5 == True", "((3 < 5) == True)"),\
                ("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"), ("(5 + 5) * 2", "((5 + 5) * 2)"), 
                ("2 / (5 + 5)","(2 / (5 + 5))",), ("-(5 + 5)", "(-(5 + 5))"), ("!(true == true)","(!(True == True))"),\
                ("add(a * b[2], b[1], 2 * [1, 2][1])", "add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))",)]

        for inp, expexted in tests:
            l = new_lexer(inp)
            p = Parser(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            self.assertTrue(str(program) == expexted, f"expected {expexted}. But got {str(program)}")

    def validate_integer_literal(self, right: Expression, int_val: int):
        self.assertTrue(isinstance(right, IntegerLiteral), f'right is a {type(right)}. Not an IntegerLiteral.')
        il: IntegerLiteral = right
        self.assertTrue(il.value == int_val, f"il.value is {il.value} != {int_val}")
        self.assertTrue(il.token_literal() == str(int_val), f"il.token_literal() is {il.token_literal()} != {int_val}")


    def test_boolean_expressions(self):
        inputs = ['true', 'false']
        values = [True, False]

        for i, inp in enumerate(inputs):
            l = new_lexer(inp)
            p = Parser(l)
            program = p.parse_program()
            self.check_parse_errors(p)

            self.assertTrue(len(program.statements) == 1, f"Expected 1 statement. Got {len(program.statements)} instead")
            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, ExpressionStatement), f"stmt is not an ExpressionStatement. Its a {type(stmt)}")
            exp_stmt: ExpressionStatement = stmt

            self.validate_boolean_expression(exp_stmt.expression, values[i])

    def validate_boolean_expression(self, exp: Expression, value: bool):
        self.assertTrue(isinstance(exp, Boolean), f"exp is not a Boolean. Its a {type(exp)}")
        bool_exp: Boolean = exp

        self.assertTrue(bool_exp.token_literal() == str(value).lower(), f"bool_exp.token_literal() = {bool_exp.token_literal()} != {str(value).lower()}")
        self.assertTrue(bool_exp.value == value, f"bool_exp.value = {bool_exp.value} != True")


    # dont see. The code in both of them is repeated and its ugly 🫣
    def test_if_expression(self):
        inp = 'if (x < y) { x }'
        l = new_lexer(inp)
        p = Parser(l)

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(len(program.statements) == 1, f"len(program.statements) = {len(program.statements)} != 1")
        stmt = program.statements[0]
        
        self.assertTrue(isinstance(stmt, ExpressionStatement), f'stmt is not an ExpressionStatement. Its a {type(stmt)}')
        exp_stmt: ExpressionStatement = stmt
        exp = exp_stmt.expression
        self.assertTrue(isinstance(exp, IfExpression), f'exp_stmt.expression is not an IfExpression. Its a {type(exp)}')
        if_exp: IfExpression = exp
        self.validate_infix_expression(if_exp.condition, 'x', '<', 'y')

        self.assertTrue(len(if_exp.consequence.statements) == 1, f'len(if_exp.consequence.statements) = {len(if_exp.consequence.statements)} != 1')
        con_stmt = if_exp.consequence.statements[0]

        self.assertTrue(isinstance(con_stmt, ExpressionStatement), f'con_stmt is not ExpressionStmt. Its a {type(con_stmt)}')
        con_exp_stmt: ExpressionStatement = con_stmt

        self.validate_identifier_expression(con_exp_stmt.expression, 'x')

        if if_exp.alternative:
            self.fail(f'if_exp.alternative is expected to be None. But got {if_exp.alternative}')

    def test_if_else_exp(self):
        inp = 'if (x < y) { x } else { y }'
        l = new_lexer(inp)
        p = Parser(l)

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(len(program.statements) == 1, f"len(program.statements) = {len(program.statements)} != 1")
        stmt = program.statements[0]
        
        self.assertTrue(isinstance(stmt, ExpressionStatement), f'stmt is not an ExpressionStatement. Its a {type(stmt)}')
        exp_stmt: ExpressionStatement = stmt

        exp = exp_stmt.expression
        self.assertTrue(isinstance(exp, IfExpression), f'exp_stmt.expression is not an IfExpression. Its a {type(exp)}')

        if_exp: IfExpression = exp
        self.validate_infix_expression(if_exp.condition, 'x', '<', 'y')

        self.assertTrue(len(if_exp.consequence.statements) == 1, f'len(if_exp.consequence.statements) = {len(if_exp.consequence.statements)} != 1')
        con_stmt = if_exp.consequence.statements[0]

        self.assertTrue(isinstance(con_stmt, ExpressionStatement), f'con_stmt is not ExpressionStmt. Its a {type(con_stmt)}')
        con_exp_stmt: ExpressionStatement = con_stmt

        self.validate_identifier_expression(con_exp_stmt.expression, 'x')

        if if_exp.alternative:
            self.assertTrue(len(if_exp.alternative.statements) == 1, f'len(if_exp.alternative.statements) = {len(if_exp.alternative.statements)} != 1')
            alt_stmt = if_exp.alternative.statements[0]

            self.assertTrue(isinstance(alt_stmt, ExpressionStatement), f'alt_stmt is not ExpressionStmt. Its a {type(alt_stmt)}')
            alt_exp_stmt: ExpressionStatement = alt_stmt

            self.validate_identifier_expression(alt_exp_stmt.expression, 'y')


    def test_function_literal(self):
        inp = 'golmaal(x, y){x + y;}'
        l = new_lexer(inp)
        p = Parser(l)

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(len(program.statements) == 1, f"len(program.statements) = {len(program.statements)} != 1")
        stmt = program.statements[0]

        self.assertTrue(isinstance(stmt, ExpressionStatement), f"stmt is not an ExpressionStatement. Its a {type(stmt)}")
        exp_stmt: ExpressionStatement = stmt

        self.assertTrue(isinstance(exp_stmt.expression, FunctionLiteral), f"exp_stmt.expression is not a FunctionLiteral. Its a {type(exp_stmt.expression)}")
        func: FunctionLiteral = exp_stmt.expression

        self.assertTrue(len(func.parameters) == 2, f"func.parameters does not contain 2 parameters. It contains {len(func.parameters)}")
        self.validate_identifier_expression(func.parameters[0], 'x')
        self.validate_identifier_expression(func.parameters[1], 'y')

        self.assertTrue(len(func.body.statements) == 1, f"func.body.statements does not contain 1 statement. It contains {len(func.body.statements)}")
        body_stmt = func.body.statements[0]

        self.assertTrue(isinstance(body_stmt, ExpressionStatement), f"body_stmt is not an ExpressionStatement. Its a {type(body_stmt)}")
        body_exp_stmt: ExpressionStatement = body_stmt

        self.validate_infix_expression(body_exp_stmt.expression, 'x', '+', 'y')

    def test_function_params(self):
        inps = [('golmaal(){}', []), ('golmaal(x,){x}', ['x']), ('golmaal(x, y, z,){x+y+z;}', ['x', 'y', 'z'])]
        for i, (inp, expected) in enumerate(inps):
            l = new_lexer(inp)
            p = Parser(l)

            program = p.parse_program()
            self.check_parse_errors(p)

            self.assertTrue(len(program.statements) == 1, f"len(program.statements) = {len(program.statements)} != 1")
            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, ExpressionStatement), f'stmt {i} is not an ExpressionStatement. Its a {type(stmt)}')
            exp_stmt: ExpressionStatement = stmt

            self.assertTrue(isinstance(exp_stmt.expression, FunctionLiteral), f'exp_stmt {i} is not a FunctionLiteral. Its a {type(exp_stmt)}')            
            exp: FunctionLiteral = exp_stmt.expression

            self.assertTrue(len(exp.parameters) == len(expected), f'len(exp.parameters) = {len(exp.parameters)} != {len(expected)}')       
            parameters = exp.parameters
            for i, param in enumerate(expected):
                self.assertTrue(isinstance(parameters[i], Identifier), f"parameters[i] is not an Identifier. Its a {type(parameters[i])}")
                self.assertTrue(parameters[i].token_literal() == param, f'parameters[i].token_literal() = {parameters[i].token_literal()} != {param}')                


    def test_call_expression(self):
        # add() add(foobar) add(2, golmaal(x, y){x+y}(2, 3)) add(2, 3*5, 4+8)
        inps = ['add()', 'add(foobar)', 'add(2, golmaal(x, y){x+y}(2, 3))', 'add(2, 3*5, 4+8)']
        for i, inp in enumerate(inps):
            l = new_lexer(inp)
            p = Parser(l)

            program = p.parse_program()
            self.check_parse_errors(p)

            self.assertTrue(len(program.statements) == 1, f'len(program.statements) = {len(program.statements)} != 1')
            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, ExpressionStatement), f'stmt {i} is not an ExpressionStatement. Its a {type(stmt)}')
            exp_stmt: ExpressionStatement = stmt

            self.assertTrue(isinstance(exp_stmt.expression, CallExpression), f'exp_stmt.expression {i} is not a CallExpression. Its a {type(exp_stmt.expression)}')            
            exp: CallExpression = exp_stmt.expression

            self.validate_identifier_expression(exp.function, 'add')
            args = exp.arguments

            self.assertTrue(len(args) == i, f'len(args) = {len(args)} != {i}')
            match i:
                case 0:
                    continue
                case 1:
                    self.validate_identifier_expression(args[0], 'foobar')
                case 2:
                    self.validate_integer_literal(args[0], 2)
                    self.assertTrue(isinstance(args[1], CallExpression), f'arg2 is not a CallExpression. Its a {type(args[1])}')
                    arg2: CallExpression = args[1]
                    arg2_args = arg2.arguments
                    self.validate_integer_literal(arg2_args[0], 2)
                    self.validate_integer_literal(arg2_args[1], 3)
                case _:
                    self.validate_integer_literal(args[0], 2)
                    self.validate_infix_expression(args[1], 3, '*', 5)
                    self.validate_infix_expression(args[2], 4, '+', 8)


    def test_string_literal(self):
        inps = ['"foobar";', '"sagar gupta";', '"om sai ram";']
        exp = ['foobar', 'sagar gupta', 'om sai ram']
        for i, inp in enumerate(inps):
            l = new_lexer(inp)
            p = Parser(l)

            program = p.parse_program()
            self.check_parse_errors(p)

            self.assertTrue(len(program.statements) == 1, f'len(program.statements) = {len(program.statements)} != 1')
            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, ExpressionStatement), f'type(stmt) = {type(stmt)} != ExpressionStatement')
            exp_stmt: ExpressionStatement = stmt
            self.validate_string_literal(exp_stmt.expression, exp[i], idx = i)            

    def validate_string_literal(self, exp: Expression, value: str, idx: int = -1):
        self.assertTrue(isinstance(exp, StringExpression), f'exp -> {idx} is not a StringExpression. Its a {type(exp)}')
        str_exp: StringExpression = exp
        self.assertTrue(str_exp.value == value, f'str_exp.value -> {idx} = {str_exp.value} != {value}')

    def test_array_literals(self):
        inps = [
            '[]',
            '[1, 1*2, golmaal(x, y){x+y}, false]'
        ]

        for i, inp in enumerate(inps):
            l = new_lexer(inp)
            p = Parser(l)

            program = p.parse_program()
            self.check_parse_errors(p)

            self.assertTrue(len(program.statements) == 1, f'len(program.statements) = {len(program.statements)} != 1')
            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, ExpressionStatement), f'stmt {i} is not an ExpressionStatement. Its a {type(stmt)}')
            exp_stmt: ExpressionStatement = stmt

            self.assertTrue(isinstance(exp_stmt.expression, ArrayLiteral), f'exp_stmt.expression {i} is not an ArrayLiteral. Its a {type(exp_stmt.expression)}')
            array: ArrayLiteral = exp_stmt.expression

            match i:
                case 0:
                    self.assertTrue(len(array.elements) == 0, f'len(array.elements) = {len(array.elements)} != 0')
                case 1:
                    self.assertTrue(len(array.elements) == 4, f'len(array.elements) = {len(array.elements)} != 4')
                    self.validate_integer_literal(array.elements[0], 1)
                    self.validate_infix_expression(array.elements[1], 1, '*', 2)
                    self.assertTrue(isinstance(array.elements[2], FunctionLiteral), f'array.elements[2] is not a FunctionLiteral. Its a {type(array.elements[2])}')
                    self.validate_boolean_expression(array.elements[3], False)

    def test_index_expression(self):
        inp = 'myarray[1+2]'

        l = new_lexer(inp)
        p = Parser(l)
        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(len(program.statements) == 1, f'len(program.statements) = {len(program.statements)} != 1')
        stmt = program.statements[0]
        self.assertTrue(isinstance(stmt, ExpressionStatement), f'stmt is not an ExpressionStatement. Its a {type(stmt)}')
        
        exp_stmt: ExpressionStatement = stmt
        self.assertTrue(isinstance(exp_stmt.expression, IndexExpression), f'exp_stmt.expression is not an IndexExpression. Its a {type(exp_stmt.expression)}')
        index_exp: IndexExpression = exp_stmt.expression

        self.validate_identifier_expression(index_exp.left, 'myarray')
        self.validate_infix_expression(index_exp.index, 1, '+', 2)


    def test_assignment_operation(self):
        inps = [
            'x = 10;',
            'x = 10 * 9 + 3;',
            'y = true;',
            'z = "hello";',
            'arr = [1, 2, 3];',
            'x = golmaal(a, b) { a + b; };',
            'nested = golmaal(x) { x = x + 1; };'
        ]

        for i, inp in enumerate(inps):
            l = new_lexer(inp)
            p = Parser(l)

            program = p.parse_program()
            self.check_parse_errors(p)

            self.assertTrue(len(program.statements) == 1, f'len(program.statements) = {len(program.statements)} != 1')
            stmt = program.statements[0]

            self.assertTrue(isinstance(stmt, AssignmentStatement), f'stmt {i} is not an AssignmentStatement. Its a {type(stmt)}')
            assign_stmt: AssignmentStatement = stmt

            match i:
                case 0:
                    self.validate_identifier_expression(assign_stmt.left, 'x')
                    self.validate_integer_literal(assign_stmt.right, 10)
                case 1:
                    self.validate_identifier_expression(assign_stmt.left, 'x')
                    self.assertTrue(isinstance(assign_stmt.right, InfixExpression), f'assign_stmt.value is not an InfixExpression. Its a {type(assign_stmt.right)}')
                    self.assertTrue('((10 * 9) + 3)' == str(assign_stmt.right), f'assign_stmt.right = {assign_stmt.right} != ((10 * 9) + 3)')
                case 2:
                    self.validate_identifier_expression(assign_stmt.left, 'y')
                    self.validate_boolean_expression(assign_stmt.right, True)
                case 3:
                    self.validate_identifier_expression(assign_stmt.left, 'z')
                    self.validate_string_literal(assign_stmt.right, "hello")
                case 4:
                    self.validate_identifier_expression(assign_stmt.left, 'arr')
                    self.assertTrue(isinstance(assign_stmt.right, ArrayLiteral), f'assign_stmt.right is not an ArrayLiteral. Its a {type(assign_stmt.right)}')
                    self.assertTrue(len(assign_stmt.right.elements) == 3, f'len(assign_stmt.right.elements) = {len(assign_stmt.right.elements)} != 3')
                    self.validate_integer_literal(assign_stmt.right.elements[0], 1)
                    self.validate_integer_literal(assign_stmt.right.elements[1], 2)
                    self.validate_integer_literal(assign_stmt.right.elements[2], 3)
                case 5:
                    self.validate_identifier_expression(assign_stmt.left, 'x')
                    self.assertTrue(isinstance(assign_stmt.right, FunctionLiteral), f'assign_stmt.right is not a FunctionLiteral. Its a {type(assign_stmt.right)}')
                    self.assertTrue(len(assign_stmt.right.parameters) == 2, f'len(assign_stmt.right.parameters) = {len(assign_stmt.right.parameters)} != 2')
                    self.validate_identifier_expression(assign_stmt.right.parameters[0], 'a')
                    self.validate_identifier_expression(assign_stmt.right.parameters[1], 'b')
                    self.assertTrue(len(assign_stmt.right.body.statements) == 1, f'len(assign_stmt.right.body.statements) = {len(assign_stmt.right.body.statements)} != 1')
                    body_stmt = assign_stmt.right.body.statements[0]
                    self.assertTrue(isinstance(body_stmt, ExpressionStatement), f'body_stmt is not an ExpressionStatement. Its a {type(body_stmt)}')
                    self.validate_infix_expression(body_stmt.expression, 'a', '+', 'b')
                case 6:
                    self.validate_identifier_expression(assign_stmt.left, 'nested')
                    self.assertTrue(isinstance(assign_stmt.right, FunctionLiteral), f'assign_stmt.right is not a FunctionLiteral. Its a {type(assign_stmt.right)}')
                    self.assertTrue(len(assign_stmt.right.parameters) == 1, f'len(assign_stmt.right.parameters) = {len(assign_stmt.right.parameters)} != 1')
                    self.validate_identifier_expression(assign_stmt.right.parameters[0], 'x')
                    self.assertTrue(len(assign_stmt.right.body.statements) == 1, f'len(assign_stmt.right.body.statements) = {len(assign_stmt.right.body.statements)} != 1')
                    body_stmt = assign_stmt.right.body.statements[0]
                    self.assertTrue(isinstance(body_stmt, AssignmentStatement), f'body_stmt is not an AssignmentStatement. Its a {type(body_stmt)}')
                    self.validate_identifier_expression(body_stmt.left, 'x')
                    self.assertTrue(isinstance(body_stmt.right, InfixExpression), f'body_stmt.right is not an InfixExpression. Its a {type(body_stmt.right)}')
                    self.validate_infix_expression(body_stmt.right, 'x', '+', 1)


    def test_while_stmt(self):
        inps = [
            'jaadu x = 10; while(x){x = x-1;}',
            'jaadu y = 5; while(y > 0){y = y - 1;}',
            'jaadu z = 0; while(z < 3){z = z + 1;}',
            'jaadu a = true; while(a){a = false;}',
            'jaadu b = 0; while(b < 10){if(b == 5){b = b + 2;} else {b = b + 1;}}'
        ]

        for i, test in enumerate(inps):
            l = new_lexer(test)
            p = Parser(l)
            program = p.parse_program()
            self.check_parse_errors(p)

            match i:
                case 0:
                    self.assertTrue(len(program.statements) == 2, f'len(program.statements) = {len(program.statements)} != 2')
                    stmt = program.statements[1]
                    self.assertTrue(isinstance(stmt, WhileStatement), f'stmt is not a WhileStatement. Its a {type(stmt)}')
                    whl_stmt: WhileStatement = stmt
                    self.validate_identifier_expression(whl_stmt.condition, 'x')
                    self.assertTrue(len(whl_stmt.body.statements) == 1, f'len(whl_stmt.body.statements) = {len(whl_stmt.body.statements)} != 1')
                    self.assertTrue(isinstance(whl_stmt.body.statements[0], AssignmentStatement), f'whl_stmt.body.statements[0] is not an AssignmentStatement. Its a {type(whl_stmt.body.statements[0])}')
                    ass_stmt: AssignmentStatement = whl_stmt.body.statements[0]
                    self.validate_identifier_expression(ass_stmt.left, 'x')
                    self.validate_infix_expression(ass_stmt.right, 'x', '-', 1)
                case 1:
                    self.assertTrue(len(program.statements) == 2, f'len(program.statements) = {len(program.statements)} != 2')
                    stmt = program.statements[1]
                    self.assertTrue(isinstance(stmt, WhileStatement), f'stmt is not a WhileStatement. Its a {type(stmt)}')
                    whl_stmt: WhileStatement = stmt
                    self.validate_infix_expression(whl_stmt.condition, 'y', '>', 0)
                    self.assertTrue(len(whl_stmt.body.statements) == 1, f'len(whl_stmt.body.statements) = {len(whl_stmt.body.statements)} != 1')
                    ass_stmt: AssignmentStatement = whl_stmt.body.statements[0]
                    self.validate_identifier_expression(ass_stmt.left, 'y')
                    self.validate_infix_expression(ass_stmt.right, 'y', '-', 1)
                case 2:
                    self.assertTrue(len(program.statements) == 2, f'len(program.statements) = {len(program.statements)} != 2')
                    stmt = program.statements[1]
                    self.assertTrue(isinstance(stmt, WhileStatement), f'stmt is not a WhileStatement. Its a {type(stmt)}')
                    whl_stmt: WhileStatement = stmt
                    self.validate_infix_expression(whl_stmt.condition, 'z', '<', 3)
                    self.assertTrue(len(whl_stmt.body.statements) == 1, f'len(whl_stmt.body.statements) = {len(whl_stmt.body.statements)} != 1')
                    ass_stmt: AssignmentStatement = whl_stmt.body.statements[0]
                    self.validate_identifier_expression(ass_stmt.left, 'z')
                    self.validate_infix_expression(ass_stmt.right, 'z', '+', 1)
                case 3:
                    self.assertTrue(len(program.statements) == 2, f'len(program.statements) = {len(program.statements)} != 2')
                    stmt = program.statements[1]
                    self.assertTrue(isinstance(stmt, WhileStatement), f'stmt is not a WhileStatement. Its a {type(stmt)}')
                    whl_stmt: WhileStatement = stmt
                    self.validate_identifier_expression(whl_stmt.condition, 'a')
                    self.assertTrue(len(whl_stmt.body.statements) == 1, f'len(whl_stmt.body.statements) = {len(whl_stmt.body.statements)} != 1')
                    ass_stmt: AssignmentStatement = whl_stmt.body.statements[0]
                    self.validate_identifier_expression(ass_stmt.left, 'a')
                    self.validate_boolean_expression(ass_stmt.right, False)
                case 4:
                    self.assertTrue(len(program.statements) == 2, f'len(program.statements) = {len(program.statements)} != 2')
                    stmt = program.statements[1]
                    self.assertTrue(isinstance(stmt, WhileStatement), f'stmt is not a WhileStatement. Its a {type(stmt)}')
                    whl_stmt: WhileStatement = stmt
                    self.validate_infix_expression(whl_stmt.condition, 'b', '<', 10)
                    self.assertTrue(len(whl_stmt.body.statements) == 1, f'len(whl_stmt.body.statements) = {len(whl_stmt.body.statements)} != 1')
                    if_stmt = whl_stmt.body.statements[0].expression
                    self.assertTrue(isinstance(if_stmt, IfExpression), f'if_stmt is not an IfExpression. Its a {type(if_stmt)}')
                    self.validate_infix_expression(if_stmt.condition, 'b', '==', 5)
                    self.assertTrue(len(if_stmt.consequence.statements) == 1, f'len(if_stmt.consequence.statements) = {len(if_stmt.consequence.statements)} != 1')
                    cons_stmt: AssignmentStatement = if_stmt.consequence.statements[0]
                    self.validate_identifier_expression(cons_stmt.left, 'b')
                    self.validate_infix_expression(cons_stmt.right, 'b', '+', 2)
                    self.assertTrue(len(if_stmt.alternative.statements) == 1, f'len(if_stmt.alternative.statements) = {len(if_stmt.alternative.statements)} != 1')
                    alt_stmt: AssignmentStatement = if_stmt.alternative.statements[0]
                    self.validate_identifier_expression(alt_stmt.left, 'b')
                    self.validate_infix_expression(alt_stmt.right, 'b', '+', 1)


    def check_parse_errors(self, p: Parser):
        errors = p.errors

        if not len(errors):
            return
        
        print(f"Parser has {len(errors)} errors")

        for i, error in enumerate(errors):
            print(f"Error {i}: {error}")

        self.fail()
    



if __name__ == "__main__":
    unittest.main() 