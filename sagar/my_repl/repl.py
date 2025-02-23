from sagar.my_token.token import Token, Constants
from sagar.lexer import Lexer

PROMPT = ">>"

def start():
    while True:
        line = input(PROMPT)
        l = Lexer.new_lexer(line)
        con = Constants()

        tok = l.next_token()
        while tok.token_type != con.EOF:
            print(tok)
            tok = l.next_token()


