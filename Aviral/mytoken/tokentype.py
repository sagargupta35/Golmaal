# token/tokentype.py
class TokenType:
    # Special Tokens
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + literals
    IDENT = "IDENT"
    INT = "INT"

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="

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
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"

    # Keyword mapping
    keywords = {
        "let": LET,
        "fn": FUNCTION,
        "true": TRUE,
        "false": FALSE,
        "if": IF,
        "else": ELSE,
        "return": RETURN
    }

    @staticmethod
    def get_ident_type(s):
        return TokenType.keywords.get(s, TokenType.IDENT)
