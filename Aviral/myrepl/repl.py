# repl/repl.py
from Aviral.mylexer.lexer import Lexer
from Aviral.mytoken.token import Token
from Aviral.mytoken.tokentype import TokenType
PROMPT = ">> "

def start():
    while True:
        try:
            line = input(PROMPT)
        except EOFError:
            return

        lexer = Lexer(line)

        while True:
            tok = lexer.next_token()
            if tok.type == "EOF":
                break
            if tok.type == "ILLEGAL":
                print(f"ILLEGAL token at: {tok.literal}")
                break
            else:
                print(f"{tok.type} {tok.literal}")

