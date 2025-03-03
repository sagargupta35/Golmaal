import unittest
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_ast.ast import Statement, LetStatement, ReturnStatement, ExpressionStatement, Identifier, IntegerLiteral

class TestParser(unittest.TestCase):
    def test_let_statement(self):
        input = '''
            let five = 5;
            let ten = 10;
            let foobar = 838383;
        '''

        l = new_lexer(input)
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
        input = '''
            return 10;
            return 5;
            return 342934923;
        '''

        l = new_lexer(input)
        p = Parser(lexer=l)

        program = p.parse_program()
        self.check_parse_errors(p)

        self.assertTrue(program != None, "p.parse_program() returned null.")
        self.assertTrue(len(program.statements) == 3, f"Expected 3 statements. But found {len(program.statements)} statements")
        
        for i, stmt in enumerate(program.statements):
            self.assertTrue(stmt.token_literal() == 'return', f"Expected return as token_literal. But found {stmt.token_literal()}")
            self.assertTrue(isinstance(stmt, ReturnStatement), f"stmt {i} is not an instance of ReturnStatment")


    def test_identifier_expression(self):
        input = 'foobar;'

        l = new_lexer(input)
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
        input = '''
            5;
            9379;
        '''

        values = [5, 9379]

        l = new_lexer(input=input)
        p = Parser(l)

        program = p.parse_program()
        self.assertTrue(program != None, "p.parse_program() returned None")
        self.assertTrue(len(program.statements) == 2, f"Expected 2 statments. But found {len(program.statements)}")

        for i, stmt in enumerate(program.statements):
            self.assertTrue(isinstance(stmt, ExpressionStatement), f"stmt {i} is not an Expression statment. Its a {type(stmt)}")
            exp_stmt: ExpressionStatement = stmt
            self.assertTrue(isinstance(exp_stmt.expression, IntegerLiteral), f"exp_stmt.expression is not an IntegerLiteral. Its a {type(exp_stmt.expression)}")
            exp: IntegerLiteral = exp_stmt.expression
            self.assertTrue(exp.value == values[i], f"exp.value != {values[i]}. Its {exp.value}")
            self.assertTrue(exp.token_literal() == f"{values[i]}", f'exp.token_literal() != "{values[i]}". It is {exp.token_literal()}')
            

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