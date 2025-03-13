import unittest
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_evaluator.evaluator import eval
from sagar.my_object.object import *


class TestEvaluator(unittest.TestCase):

    def test_eval_integer_expression(self):
        inps = [("5", 5),
                ("10", 10),
                ("-5",-5),
                ("-10",-10),
                ("5 + 5 + 5 + 5- 10", 10),
                ("2 * 2 * 2 * 2 * 2", 32),
                ("-50 + 100 +-50", 0),
                ("5 * 2 + 10", 20),
                ("5 + 2 * 10", 25),
                ("20 + 2 *-10", 0),
                ("50 / 2 * 2 + 10", 60),
                ("2 * (5 + 10)", 30),
                ("3 * 3 * 3 + 10", 37),
                ("3 * (3 * 3) + 10", 37),
                ("(5 + 10 * 2 + 15 / 3) * 2 +-10", 50),
            ]
        for i, (inp, exp) in enumerate(inps):
            evaluated: Object = self.get_eval(inp)
            self.validate_integer_obj(evaluated, exp, i)

    def validate_integer_obj(self, obj: Object, value: int, idx: int = -1):
        self.assertTrue(isinstance(obj, IntegerObj), f'obj -> {idx} is not an IntegerObj. It is a {str(obj)}')
        int_obj: IntegerObj = obj
        self.assertTrue(int_obj.value == value, f'int_obj.value -> {idx} = {int_obj.value} != {value}')


    def test_eval_boolean_expression(self):
        inps = [('true', True), ('false', False)]
        for i, (inp, exp) in enumerate(inps):
            evaluated: Object = self.get_eval(inp)
            self.validate_boolean_obj(evaluated, exp, idx = i)

    def test_bang_operator(self):
        inps = [("true", True),
                ("false", False),
                ("1 < 2", True),
                ("1 > 2", False),
                ("1 < 1", False),
                ("1 > 1", False),
                ("1 == 1", True),
                ("1 != 1", False),
                ("1 == 2", False),
                ("1 != 2", True),]
        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.validate_boolean_obj(evaluated, exp, idx = i)

    def validate_boolean_obj(self, obj: Object, value: bool, idx: int = -1):
        self.assertTrue(isinstance(obj, BooleanObj), f'obj is not an BooleanObj. It is a {str(obj)}')
        bool_obj: BooleanObj = obj
        self.assertTrue(bool_obj.value == value, f'bool_obj.value->{idx} = {bool_obj.value} != {value}')        


    def test_if_else_exp(self):
        inps = [
            ("if (true) { 10 }", 10),
            ("if (false) { 10 }", None),
            ("if (1) { 10 }", 10),
            ("if (1 < 2) { 10 }", 10),
            ("if (1 > 2) { 10 }", None),
            ("if (1 > 2) { 10 } else { 20 }", 20),
            ("if (1 < 2) { 10 } else { 20 }", 10),
        ]

        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            if not exp:
                if not isinstance(evaluated, NullObj):
                    self.fail(f'evaluated is expected to be NullObj. It is {evaluated}')
            else:
                self.validate_integer_obj(evaluated, value=exp, idx=i)


    def get_eval(self, inp: str) -> Object:
        l = new_lexer(inp)
        p = Parser(l)

        program = p.parse_program()
        return eval(program)
    

if __name__ == '__main__':
    unittest.main()