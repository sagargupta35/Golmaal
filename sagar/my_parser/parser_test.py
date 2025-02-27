import unittest
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_ast.ast import Statement, LetStatement

class TestParser(unittest.TestCase):
    def test_parser(self):
        input = '''
            let five = 5;
            let ten = 10;
            let foobar = 838383;
        '''

        l = new_lexer(input)
        p = Parser(lexer= l)

        identifiers = ['five', 'ten', 'foobar']

        program = p.parse_program()
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


if __name__ == "__main__":
    unittest.main()