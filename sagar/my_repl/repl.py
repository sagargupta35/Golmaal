from sagar.my_token.token import Token, Constants
from sagar.lexer import Lexer
from sagar.my_parser.parser import Parser

PROMPT = "##"

def start():
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

        print(str(program))


