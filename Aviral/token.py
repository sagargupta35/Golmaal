# token/token.py
from dataclasses import dataclass

# Define TokenType as a simple string alias
TokenType = str

# Token dataclass
@dataclass
class Token:
    type: TokenType
    literal: str

# Constants class to hold all token types
class Constants:
    # Token Types
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + literals
    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"      # 1343456

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

