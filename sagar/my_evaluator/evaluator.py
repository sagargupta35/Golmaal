from sagar.my_ast.ast import *
from sagar.my_object.object import *
from dataclasses import dataclass

@dataclass(frozen=True)
class EvalConstants:
    TRUE_BOOLEAN_OBJ = BooleanObj(True)
    FALSE_BOOLEAN_OBJ = BooleanObj(False)
    NULL_OBJ = NullObj()


def eval(node: Node) -> Object:
    
    if isinstance(node, Program):
        return eval_statements(node.statements)
    
    elif isinstance(node, ExpressionStatement):
        return eval(node.expression)

    elif isinstance(node, IntegerLiteral):
        return IntegerObj(value=node.value)

    elif isinstance(node, Boolean):
        if node.value:
            return EvalConstants.TRUE_BOOLEAN_OBJ # As all boolean true objs are same follow singleton approach
        else:
            return EvalConstants.FALSE_BOOLEAN_OBJ
    
    elif isinstance(node, PrefixExpression):
        right = eval(node.right)
        return eval_prefix_expression(node.operator, right)
    
    elif isinstance(node, InfixExpression):
        left = eval(node.left)
        right = eval(node.right)
        return eval_infix_expression(node.operator, left, right)

    elif isinstance(node, BlockStatement):
        return eval_block_statements(node.statements)
    
    elif isinstance(node, IfExpression):
        return eval_if_expression(node)
    
    elif isinstance(node, ReturnStatement):
        value = eval(node.value)
        return ReturnObj(value=value)
    
    return EvalConstants.NULL_OBJ


def eval_statements(statements: list[Statement]) -> Object:

    for statement in statements:
        res = eval(statement)

        if isinstance(res, ReturnObj):
            return res.value

    return res

def eval_block_statements(statements: list[Statement]) -> Object:
    for statement in statements:
        res = eval(statement)

        if isinstance(res, ReturnObj):
            return res

    return res

def eval_prefix_expression(operator: str, right: Object) -> Object:

    if operator == '!':
        return eval_bang_operator(right)
    
    elif operator == '-':
        return eval_minus_operator(right)
    
    return EvalConstants.NULL_OBJ

def eval_minus_operator(right: Object) -> Object:

    if isinstance(right, IntegerObj):
        return IntegerObj(-right.value)
    
    return EvalConstants.NULL_OBJ

def eval_bang_operator(right: Object) -> Object:

    if isinstance(right, BooleanObj):
        if right is EvalConstants.TRUE_BOOLEAN_OBJ:
            return EvalConstants.FALSE_BOOLEAN_OBJ
        return EvalConstants.TRUE_BOOLEAN_OBJ
    elif isinstance(right, IntegerObj):
        if right.value > 0:
            return EvalConstants.FALSE_BOOLEAN_OBJ
        return EvalConstants.TRUE_BOOLEAN_OBJ
    elif isinstance(right, NullObj):
        return EvalConstants.TRUE_BOOLEAN_OBJ
    
    return EvalConstants.NULL_OBJ

def eval_infix_expression(operator: str, left: Object, right: Object) -> Object:
    if operator in ['+', '-', '*', '/', '>', '<', '!=', '==']:
        # handle non integer cases
        if not isinstance(left, IntegerObj):
            return EvalConstants.NULL_OBJ
        if not isinstance(right, IntegerObj):
            return EvalConstants.NULL_OBJ
        
        if operator == '+':
            return IntegerObj(left.value + right.value)
        
        if operator == '-':
            return IntegerObj(left.value - right.value)
        
        if operator == '*':
            return IntegerObj(left.value * right.value)
        
        if operator == '/':
            return IntegerObj(left.value // right.value)
        
        if operator == '>':
            return BooleanObj(left.value > right.value)
        
        if operator == '<':
            return BooleanObj(left.value < right.value)
        
        if operator == '!=':
            return BooleanObj(left.value != right.value)
        
        if operator == '==':
            return BooleanObj(left.value == right.value)
    
    return EvalConstants.NULL_OBJ


def eval_if_expression(exp: IfExpression):
    condition = eval(exp.condition)

    truthy = is_truthy(condition)
    if isinstance(truthy, NullObj):
        return truthy

    if condition.value:
        return eval(exp.consequence)
    elif exp.alternative:
        return eval(exp.alternative)

    return EvalConstants.NULL_OBJ


def is_truthy(obj: Object):
    if isinstance(obj, NullObj):
        return False
    if isinstance(obj, BooleanObj):
        return obj
    if isinstance(obj, IntegerObj):
        if obj.value > 0:
            return EvalConstants.TRUE_BOOLEAN_OBJ
        return EvalConstants.FALSE_BOOLEAN_OBJ
    
    return EvalConstants.NULL_OBJ
