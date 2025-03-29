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
            ('foobar', 'identifier not found: foobar'),
            ('print(a)', 'identifier not found: a'),
            ('while(true){print(3)}', 'Cannot print more than 1000 statements currently.')
            
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

    def test_array_literals(self):
        inp = '[1, 2 * 2, 3 + 3]'

        evaluated = self.get_eval(inp)
        self.assertTrue(isinstance(evaluated, ArrayObj), f'evaluated is not an ArrayObj. Its a {type(evaluated)}')

        arr: ArrayObj = evaluated
        self.assertTrue(len(arr.elements) == 3, f'len(arr.elements) = {len(arr.elements)} != 3')

        self.validate_integer_obj(arr.elements[0], 1, 0)
        self.validate_integer_obj(arr.elements[1], 4, 1)
        self.validate_integer_obj(arr.elements[2], 6, 2)


    def test_assignment_statement(self):
        inps = [
            ('let x = 10; x = 5; x;', 5),
            ('let x = 10; x = x + 5; x;', 15),
            ('let x = 10; let y = 20; x = y; x;', 20),
            ('let x = 10; let y = 20; x = y + 10; x;', 30),
            ('let x = 10; x = x * 2; x;', 20),
            ('let x = 10; if (x > 5) { x = 15; }; x;', 15),
            ('let x = 10; if (x < 5) { x = 15; } else { x = 20; }; x;', 20),
            ('let x = 10; let y = 5; if (x > y) { x = x + y; }; x;', 15),
            ('let x = 10; x = x - 5; x;', 5),
            ('let x = 10; x = x / 2; x;', 5),
            ('let x = 10; x = x + 5 * 2; x;', 20),
            ('let x = 10; x = x + (5 * 2); x;', 20),
            ('let x = 10; x = x + (5 * 2) - 5; x;', 15),
            ('let x = 10; let y = 5; x = x + y * 2; x;', 20),
            ('let x = 10; let y = 5; x = x + (y * 2); x;', 20),
            ('let x = 10; let y = 5; x = x + (y * 2) - y; x;', 15),
        ]

        for i, (inp, exp) in enumerate(inps):
            evaluated = self.get_eval(inp)
            self.validate_integer_obj(evaluated, value=exp, idx=i)

    def test_print_statements(self):
        tests = [
            ('let a = 10; print(a);', ['10']),
            ('let a = 10; let b = 20; print(a, b);', ['10', '20']),
            ('let a = 10; let b = 20; let c = a + b; print(c);', ['30']),
            ('print("Hello, World!");', ['Hello, World!']),
            ('let a = "Hello"; let b = "World"; print(a + " " + b);', ['Hello World']),
            ('let a = [1, 2, 3]; print(a);', ['[1, 2, 3]']),
            ('let a = fn(x) { x * 2; }; print(a(5));', ['10']),
            ('if (true) { print("Condition is true"); }', ['Condition is true']),
            ('if (false) { print("Condition is false"); } else { print("Condition is true"); }', ['Condition is true']),
            ('let a = 10; if (a > 5) { print("a is greater than 5"); }', ['a is greater than 5']),
            ('let a = 10; let b = 20; if (a < b) { print("a is less than b"); } else { print("a is not less than b"); }', ['a is less than b']),
            ('let a = 10; let b = 20; print(a, b, a + b);', ['10', '20', '30']),
            ('let a = 10; let b = 20; let c = a * b; print(a, b, c);', ['10', '20', '200']),
            ('let a = 10; let b = 20; let c = a * b; print(a, b, c, c / a);', ['10', '20', '200', '20']),
        ]

        for i, (test, exp) in enumerate(tests):
            env = Environment(print_statements=[])
            l = new_lexer(test)
            p = Parser(l)
            program = p.parse_program()
            eval(program, env)
            self.assertTrue(len(env.print_statements) == len(exp), f'len(env.print_statements) -> {i} = {len(env.print_statements)} != {len(exp)}')
            for j, s in enumerate(exp):
                self.assertTrue(env.print_statements[j] == s, f'env.print_statements[{j}] = {env.print_statements[j]} != {s}')

    def test_while_statement(self):
        tests = [
            'let x = 10; while(x){x = x-1;}; print(x);',
            'let x = 5; let y = 0; while(x){y = y + x; x = x - 1;}; print(y);',
            'let x = 0; while(x < 5){x = x + 1;}; print(x);',
            'let x = 10; let y = 0; while(x > 5){y = y + x; x = x - 1;}; print(x, y);',
            'let x = 3; let y = 1; while(x > 0){y = y * x; x = x - 1;}; print(y);',
            'let x = 10; while(x > 0){if(x == 5){break;}; x = x - 1;}; print(x);',
            'let x = 10; let y = 0; while(x > 0){if(x == 5){x = x - 1; continue;}; y = y + x; x = x - 1;}; print(y);',
        ]
        expected_outputs = [
            ['0'],
            ['15'],
            ['5'],
            ['5', '40'],
            ['6'],
            ['5'],
            ['50'],
        ]

        for i, (test, exp) in enumerate(zip(tests, expected_outputs)):
            env = Environment(print_statements=[])
            l = new_lexer(test)
            p = Parser(l)
            program = p.parse_program()

            evaluated = eval(program, env)
            if isinstance(evaluated, ErrorObj):
                print(evaluated.message)
            self.assertTrue(isinstance(evaluated, NullObj), f'evaluated -> {i} is not a NullObj. Its a {type(evaluated)}')

            self.assertTrue(len(env.print_statements) == len(exp), f'len(env.print_statements) -> {i} = {len(env.print_statements)} != {len(exp)}')
            for j, s in enumerate(exp):
                self.assertTrue(env.print_statements[j] == s, f'env.print_statements[{j}] -> {i} = {env.print_statements[j]} != {s}')

    def test_index_expression(self):
        tests = [
            'let x = 10; while(x > 0){x = x-1;}; let arr = [1, 2, 3]; print(arr[x])',
            'let arr = [1, 2, 3, 4, 5]; print(arr[0])',
            'let arr = [1, 2, 3, 4, 5]; print(arr[4])',
            'let arr = [1, 2, 3, 4, 5]; print(arr[2])',
            'let arr = [1, 2, 3]; let idx = 1; print(arr[idx])',
            'let arr = [1, 2, 3]; let idx = 2; print(arr[idx])',
            'let arr = [1, 2, 3]; print(arr[3])',  # Out of bounds
            'let arr = [1, 2, 3]; print(arr[-1])',  # Negative index
            'let arr = [1, 2, 3]; let idx = "1"; print(arr[idx])',  # Invalid index type
            'let arr = []; print(arr[0])',  # Empty array
            'let x = 10; print(x[3])' # Invalid array type
        ]
        exp = [
            ['1'],
            ['1'],
            ['5'],
            ['3'],
            ['2'],
            ['3'],
            ['Array index out of bounds for length 3: 3'],
            ['Array index out of bounds for length 3: -1'],
            ['cannot index an array with non-integer types: STRING'],
            ['Array index out of bounds for length 0: 0'],
            ['INTEGER cannot be subscripted']
        ]
        for i, test in enumerate(tests):
            evaluated, env = self.get_eval_env(test)
            if isinstance(evaluated, ErrorObj):
                self.assertTrue(evaluated.message == exp[i][0], f'evaluated.message -> {i} = {evaluated.message} != {exp[i][0]}')
            else:
                self.assertTrue(env.print_statements == exp[i], f'env.print_statements -> {i} = {env.print_statements} != {exp[i]}')


    def get_eval_env(self, inp: str):
        l = new_lexer(inp)
        p = Parser(l)
        program = p.parse_program()

        env = Environment(print_statements=[])
        evaluated = eval(program, env)
        return evaluated, env
    
    def get_eval(self, inp: str) -> Object:
        l = new_lexer(inp)
        p = Parser(l)

        program = p.parse_program()
        return eval(program, Environment(print_statements=[]))
    

if __name__ == '__main__':
    unittest.main()