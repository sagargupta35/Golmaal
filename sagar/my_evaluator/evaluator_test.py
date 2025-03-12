import unittest
from sagar.lexer.Lexer import new_lexer
from sagar.my_parser.parser import Parser
from sagar.my_evaluator.evaluator import eval
from sagar.my_object.object import *


class TestEvaluator(unittest.TestCase):

    def test_eval_integer_expression(self):
        inps = [("5", 5), ("10", 10)]
        for (inp, exp) in inps:
            evaluated: Object = self.get_eval(inp)
            self.validate_integer_obj(evaluated, exp)

    def validate_integer_obj(self, obj: Object, value: int):
        self.assertTrue(isinstance(obj, IntegerObj), f'obj is not an IntegerObj. It is a {str(obj)}')
        int_obj: IntegerObj = obj
        self.assertTrue(int_obj.value == value, f'int_obj.value = {int_obj.value} != {value}')


    def test_eval_boolean_expression(self):
        inps = [('true', True), ('false', False)]
        for (inp, exp) in inps:
            evaluated: Object = self.get_eval(inp)
            self.validate_boolean_obj(evaluated, exp)

    def validate_boolean_obj(self, obj: Object, value: bool):
        self.assertTrue(isinstance(obj, BooleanObj), f'obj is not an BooleanObj. It is a {str(obj)}')
        bool_obj: BooleanObj = obj
        self.assertTrue(bool_obj.value == value, f'bool_obj.value = {bool_obj.value} != {value}')        


    def get_eval(self, inp: str) -> Object:
        l = new_lexer(inp)
        p = Parser(l)

        program = p.parse_program()
        return eval(program)
    

if __name__ == '__main__':
    unittest.main()