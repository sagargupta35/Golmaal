from sagar.my_token.token import Token, Constants
from sagar.lexer import Lexer
from sagar.my_parser.parser import Parser
from sagar.my_evaluator.evaluator import eval
from sagar.my_object.object import Environment, ErrorObj

PROMPT = ">>"

def start():
    env = Environment(print_statements=[])
    while True:
        line = input(PROMPT)
        if line == 'quit':
            break
        l = Lexer.new_lexer(line)
        p = Parser(l)
        program = p.parse_program()

        if len(p.errors):
            for error in p.errors:
                print(error)
            continue
        
        try:
            evaluated = eval(program, env)
        except Exception:
            print('cannot evaluate code')
            env = Environment(print_statements=[])
            
        if isinstance(evaluated, ErrorObj):
            print(evaluated.inspect())
            env.print_statements = []
            continue    
        for s in env.print_statements:
            print(s)
        env.print_statements = []


