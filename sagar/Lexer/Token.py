from dataclasses import dataclass

@dataclass
class Token:
    token_type: str
    literal: str

@dataclass(frozen=True)
class Constants:
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    #Identifiers + literals
    IDENT = "IDENT" # add, foobar, x, y, ...
    INT = "INT" # 1343456

    # Operators
    ASSIGN = "="
    PLUS = "+"

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"

constants = Constants()