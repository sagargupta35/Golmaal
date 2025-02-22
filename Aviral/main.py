# main.py
from mylexer.lexer import Lexer
from mytoken.tokentype import TokenType

def main():
    input_str = "=+(){},;"
    lexer = Lexer(input_str)

    while True:
        tok = lexer.next_token()
        print(f"Type: {tok.type}, Literal: '{tok.literal}'")
        if tok.type == TokenType.EOF:
            break

if __name__ == "__main__":
    main()
