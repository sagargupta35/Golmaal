from abc import ABC, abstractmethod
from sagar.my_token.token import Token, Constants

class Node(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

class Statement(Node):
    @abstractmethod
    def statement_node(self):
        pass

class Expression(Node):
    @abstractmethod
    def expression_node(self):
        pass

class Program(Node):
    def __init__(self):
        self.statements: list[Statement] = []

    def __str__(self):
        res = []
        for statement in self.statements:
            res.append(str(statement))
        return ''.join(res)
    
    def token_literal(self) -> str:
        if len(self.statements):
            return self.statements[0].token_literal()
        else:
            return ''

class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def __str__(self):
        return self.value
    
    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        pass


class LetStatement(Statement):
    def __init__(self, token: Token, name: Identifier, value: Expression):
        self.token: Token = token
        self.name: Identifier = name
        self.value: Expression = value

    def __str__(self) -> str:
        res: list[str] = []
        res.append('let')
        res.append(str(self.name))
        res.append('=')
        if self.value:
            res.append(str(self.value))
        return ' '.join(res)

    def token_literal(self) -> str:
        return self.token.literal
    
    def statement_node(self):
        pass

class ReturnStatement(Statement):
    def __init__(self, token: Token, value: Expression):
        self.token = token
        self.value = value

    def __str__(self) -> str:
        res = []
        res.append('return')
        if self.value:
            res.append(str(self.value))
        return ' '.join(res)

    def token_literal(self):
        return self.token.literal
    
    def statement_node(self):
        return

class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression

    def __str__(self):
        if self.expression:
            return str(self.expression)
        return ''

    def token_literal(self):
        return self.token.literal
    
    def statement_node(self):
        return
    
class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int):
        self.token = token
        self.value = value

    def __str__(self):
        return self.token.literal

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal
    

class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression):
        self.token = token
        self.operator = operator
        self.right = right

    def __str__(self):
        res = []
        res.append('(')
        res.append(self.operator)
        res.append(str(self.right))
        res.append(')')
        return ''.join(res)


    def token_literal(self):
        return self.token.literal
    
    def expression_node(self):
        pass


class InfixExpression(Expression):
    def __init__(self, token, left: Expression, operator, right: Expression):
        self.left = left
        self.token = token
        self.operator = operator
        self.right = right

    def __str__(self):
        res = []
        res.append('(')
        res.append(str(self.left) + ' ')
        res.append(str(self.operator) + ' ')
        res.append(str(self.right))
        res.append(')')
        return ''.join(res)

    def token_literal(self):
        return self.token.literal
    
    def expression_node(self):
        return None


class Boolean(Expression):
    def __init__(self, token : Token, value: bool):
        self.token = token
        self.value = value

    def expression_node(self):
        return
    
    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return str(self.value)
        

class BlockStatement(Statement):
    def __init__(self, token: Token):
        self.token = token
        self.statements: list[Statement] = []
    
    def statement_node(self):
        return
    
    def token_literal(self):
        return self.token.literal
    
    def __str__(self):
        return "; ".join(str(s) for s in self.statements)
    
class IfExpression(Expression):
    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement, alternative: BlockStatement):
        self.token: Token = token
        self.condition: Expression = condition
        self.consequence: BlockStatement = condition
        self.alternative: BlockStatement = alternative

    def expression_node(self):
        return
    
    def token_literal(self):
        return self.token.literal
    
    def __str__(self):
        res = f"if{str(self.condition)} {str(self.consequence)}"
        if self.alternative:
            res = f"{res}else {str(self.alternative)}"
        return res
        

class FunctionLiteral(Expression):
    def __init__(self, token: Token, parameters: BlockStatement = None, body: BlockStatement = None):
        self.token = token
        self.parameters: list[Identifier] = parameters
        self.body: BlockStatement = body

    def expression_node(self):
        return
    
    def token_literal(self):
        return self.token.literal
    
    def __str__(self):
        return f'{self.token_literal()}({', '.join([str(param) for param in self.parameters])}){Constants.LBRACE} {str(self.body)} {Constants.RBRACE}'
    

class CallExpression(Expression):

    def __init__(self, token: Token, function: Expression):
        self.token: Token = token
        self.function: Expression = function
        self.arguments: list[Expression] = []
    
    def expression_node(self):
        return
    
    def token_literal(self):
        return self.token.literal
    
    def __str__(self):
        res = [
            str(self.function),
            '(',
            ', '.join([str(arg) for arg in self.arguments]),
            ')'
        ]
        return ''.join(res)
    
class StringExpression(Expression):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.literal
    
    def token_literal(self):
        return self.token.literal
    
    def expression_node(self):
        return
        