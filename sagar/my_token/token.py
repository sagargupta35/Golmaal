from dataclasses import dataclass

TokenType = str

@dataclass
class Token:
    token_type: TokenType
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


keywords = {
    'let': Constants.LET,
    'fn': Constants.FUNCTION
}

def get_ident_type(ch: str) -> TokenType:
    return keywords.get(ch, Constants.IDENT)
