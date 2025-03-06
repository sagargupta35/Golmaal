import unittest
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_ast.ast import Statement, LetStatement, ReturnStatement, ExpressionStatement, Identifier, IntegerLiteral, PrefixExpression, Expression, InfixExpression

class TestParser(unittest.TestCase):
    def test_let_statement(self):
        inp = '''
            let five = 5;
            let ten = 10;
            let foobar = 838383;
        '''

        l = new_lexer(inp)
        p = Parser(lexer= l)

        identifiers = ['five', 'ten', 'foobar']

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(program != None, f"Unable to parse program. Parser returned None")
        self.assertTrue(len(program.statements) == 3, f"Expected 3 statements. But found {len(program.statements)}")

        for iden, stmt in zip(identifiers, program.statements):
            self.validate_let_statement(stmt, iden)

    def validate_let_statement(self, stmt: Statement, iden: str):
        self.assertTrue(stmt.token_literal() == 'let', f"Expected let as token literal for stmt. But found {stmt.token_literal()}")
        self.assertTrue(isinstance(stmt, LetStatement), f"stmt is not instance of LetStatement. It is a {type(stmt)}")
        letstmt: LetStatement = stmt
        self.assertTrue(letstmt.name.token_literal() == iden, f"letstmt.name.token_literal() is not {iden}. Found {letstmt.name.token_literal()}")
        self.assertTrue(letstmt.name.value == iden, f"letstmt.name.value is not {iden}. Found {letstmt.name.value}")


    def test_return_statement(self):
        inp = '''
            return 10;
            return 5;
            return 342934923;
        '''

        l = new_lexer(inp)
        p = Parser(lexer=l)

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(program != None, "p.parse_program() returned null.")
        self.assertTrue(len(program.statements) == 3, f"Expected 3 statements. But found {len(program.statements)} statements")
        
        for i, stmt in enumerate(program.statements):
            self.assertTrue(stmt.token_literal() == 'return', f"Expected return as token_literal. But found {stmt.token_literal()}")
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
        self.assertTrue(isinstance(exp_stmt.expression, Identifier), f"exp_stmt.expression is not an instance of Identifier. It is a {type(exp_stmt.expression)}")
        iden = exp_stmt.expression

        self.assertTrue(iden.value == 'foobar', f"iden.value is not 'foobar'. Found {iden.value}")
        self.assertTrue(iden.token_literal() == 'foobar', f"iden.token_literal() is not 'foobar'. Found {iden.token_literal()}")

    
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
            self.assertTrue(isinstance(exp_stmt.expression, IntegerLiteral), f"exp_stmt.expression is not an IntegerLiteral. Its a {type(exp_stmt.expression)}")
            exp: IntegerLiteral = exp_stmt.expression
            self.assertTrue(exp.value == values[i], f"exp.value != {values[i]}. Its {exp.value}")
            self.assertTrue(exp.token_literal() == f"{values[i]}", f'exp.token_literal() != "{values[i]}". It is {exp.token_literal()}')

    def test_prefix_expression(self):
        prefix_exps = [("!5;", "!", 5), ("-15;", "-", 15)]

        for inp, op, int_val in prefix_exps:
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
            self.validate_integer_literal(exp.right, int_val)

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

    def test_operator_precedence(self):
        tests = [( "-a * b", "((-a) * b)"), ("!-a", "(!(-a))"), ("a + b + c", "((a + b) + c)"),\
                  ("a + b- c", "((a + b) - c)"), ("a * b * c", "((a * b) * c)"), ("a * b / c", "((a * b) / c)"),\
                    ("a + b / c", "(a + (b / c))"), ("a + b * c + d / e- f", "(((a + (b * c)) + (d / e)) - f)"),\
                     ("3 + 4;-5 * 5", "(3 + 4)((-5) * 5)"), ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),\
                      ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),\
                       ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),\
                        ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))")]

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