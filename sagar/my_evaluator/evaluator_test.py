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
        self.assertTrue(isinstance(obj, IntegerObj), f'obj -> {idx} is not an IntegerObj. It is a {type(obj)}')
        int_obj: IntegerObj = obj
        self.assertTrue(int_obj.value == value, f'int_obj.value -> {idx} = {int_obj.value} != {value}')


    def test_eval_boolean_expression(self):
        inps = [('true', True),
                ('false', False),
                ("1 < 2", True),
                ("1 > 2", False),
                ("1 < 1", False),
                ("1 > 1", False),
                ("1 == 1", True),
                ("1 != 1", False),
                ("1 == 2", False),
                ("1 != 2", True), 
               ]
        for i, (inp, exp) in enumerate(inps):
            evaluated: Object = self.get_eval(inp)
            self.validate_boolean_obj(evaluated, exp, idx = i)

    def test_bang_operator(self):
        inps = [("!true", False),
                ("!false", True),
                ("!5", False),
                ("!!true", True),
                ("!!false", False),
                ("!!5", True),]
        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.validate_boolean_obj(evaluated, exp, idx = i)

    def validate_boolean_obj(self, obj: Object, value: bool, idx: int = -1):
        self.assertTrue(isinstance(obj, BooleanObj), f'obj {idx} is not an BooleanObj. It is a {obj.get_type()}')
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


    def test_return_statements(self):
        inps = [
            ("return 10;", 10),
            ("return 10; 9;", 10),
            ("return 2 * 5; 9;", 10),
            ("9; return 2 * 5; 9;", 10),
            ('''
                if(10 > 1){
                    if(10 > 1){
                        return 10;
                    }
                    return 1;
                }
            ''', 10)
        ]

        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.validate_integer_obj(evaluated, exp, idx=i)


    def test_error_handling(self):
        inps = [
            ('5+true;', 'type mismatch: INTEGER + BOOLEAN'),
            ('5+true; 5;', 'type mismatch: INTEGER + BOOLEAN'),
            ('-true', 'unknown operator: -BOOLEAN'),
            ('true + false', 'unknown operator: BOOLEAN + BOOLEAN'),
            ('5; true + false; 5;', 'unknown operator: BOOLEAN + BOOLEAN'),
            ("if (10 > 1) { true + false; }", "unknown operator: BOOLEAN + BOOLEAN",),
            ('''
            if (10 > 1) {
                if (10 > 1) {
                    return true + false;
                }
                return 1;
            }''', 'unknown operator: BOOLEAN + BOOLEAN'),
            ('foobar', 'identifier not found: foobar')
        ]

        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.assertTrue(isinstance(evaluated, ErrorObj), f'evaluated {i} is not an ErrorObj. Its a {type(evaluated)}')
            err_eval: ErrorObj = evaluated
            self.assertTrue(err_eval.message == exp, f'err_eval.message {i} = {err_eval.message} != {exp}')


    def test_let_statemtnts(self):
        inps = [
            ('let a = 5; a;', 5),
            ('let a = 10; let b = 5; a+b;', 15),
            ('let a = 5; let b = 6; let c = a + b; c-10;', 1)
        ]

        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.validate_integer_obj(evaluated, value=exp, idx=i)

    def test_function_object(self):
        inp = 'fn(x){return x+5;};'

        evaluated = self.get_eval(inp)
        self.assertTrue(isinstance(evaluated, FunctionObj), f'evaluated is not a FunctionObj. Its a {type(evaluated)}')
        fun: FunctionObj = evaluated

        self.assertTrue(len(fun.params) == 1, f'len(fun.params) = {len(fun.params)} != 1')
        self.assertTrue(str(fun.params[0]) == 'x', f'str(fun.params[0]) = {str(fun.params[0])} != "x"')
        
        body_str_exp = 'return (x + 5)'
        self.assertTrue(str(fun.body) == body_str_exp, f'str(fun.body) = {str(fun.body)} != {body_str_exp}')


    def test_call_expression(self):
        inps = [
            ("let identity = fn(x) { x; }; identity(5);", 5),
            ("let identity = fn(x) { return x; }; identity(5);", 5),
            ("let double = fn(x) { x * 2; }; double(5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
            ("fn(x) { x; }(5)", 5)
        ]
        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.validate_integer_obj(evaluated, value=exp, idx=i)

    def test_string_objects(self):
        inps = ['"om sai ram";', '"sagar gupta";', '"foobar"', '"om sai" + " " + "ram"', '"sagar" + ""', '"sagar " + "gupta"']
        exp = ['om sai ram', 'sagar gupta', 'foobar', 'om sai ram', 'sagar', 'sagar gupta']
        for i, inp in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.assertTrue(isinstance(evaluated, StringObj), f'evaluated -> {i} is not an instance of StringObj. Its a {type(evaluated)}')
            str_eval: StringObj = evaluated
            self.assertTrue(str_eval.value == exp[i], f'str_eval.value -> {i} = {str_eval.value} != {exp[i]}')    

    def test_len_function(self):
        tests = [
            ('len("")', 0),
            ('len("four")', 4),
            ('len("hello world")', 11),
            ('len(1)', "argument to 'len' not supported, got INTEGER"),
            ('len("one", "two")', "wrong number of arguments. got=2, want=1"),
        ]

        for i, (test, exp) in enumerate(tests):
            evaluated = self.get_eval(test)

            if isinstance(exp, int):
                self.validate_integer_obj(evaluated, exp, idx = i)
            elif isinstance(exp, str):
                self.assertTrue(isinstance(evaluated, ErrorObj), f'evaluated -> {i} is not an ErrorObj. Its a {type(evaluated)}')
                error: ErrorObj = evaluated
                self.assertTrue(error.message == exp, f'error.message -> {i} = {error.message} != {exp}')


    def get_eval(self, inp: str) -> Object:
        l = new_lexer(inp)
        p = Parser(l)

        program = p.parse_program()
        return eval(program, Environment())
    

if __name__ == '__main__':
    unittest.main()