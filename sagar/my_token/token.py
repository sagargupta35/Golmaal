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
    ASTERISK = "*"
    GT = ">"
    LT = "<"
    SLASH = "/"
    MINUS = "-"
    BANG = "!"
    EQ = "=="
    NOT_EQ = "!="

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = '['
    RBRACKET = ']'

    # Keywords
    FUNCTION = "GOLMAAL"
    LET = "MAAN_LE"
    RETURN = "YE_LO"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    STRING = 'STRING'
    WHILE = 'WHILE'

two_char_ops = {
    '==': Constants.EQ,
    '!=': Constants.NOT_EQ
}

keywords = {
    'maan_le': Constants.LET,
    'golmaal': Constants.FUNCTION,
    'true': Constants.TRUE,
    'false': Constants.FALSE,
    'if': Constants.IF,
    'else': Constants.ELSE,
    "ye_lo": Constants.RETURN,
    "while": Constants.WHILE
}

def get_two_char_type(ch: str) -> TokenType:
    return two_char_ops.get(ch, Constants.ILLEGAL)

def get_ident_type(ch: str) -> TokenType:
    return keywords.get(ch, Constants.IDENT)
