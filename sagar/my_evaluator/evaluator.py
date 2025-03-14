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
        if is_eror(right):
            return right
        return eval_prefix_expression(node.operator, right)
    
    elif isinstance(node, InfixExpression):
        left = eval(node.left)
        if is_eror(left):
            return left
        right = eval(node.right)
        if is_eror(right):
            return right
        return eval_infix_expression(node.operator, left, right)

    elif isinstance(node, BlockStatement):
        return eval_block_statements(node.statements)
    
    elif isinstance(node, IfExpression):
        return eval_if_expression(node)
    
    elif isinstance(node, ReturnStatement):
        value = eval(node.value)
        if is_eror(value):
            return value
        return ReturnObj(value=value)
    
    return ErrorObj('cannot evaluate the statement')


def eval_statements(statements: list[Statement]) -> Object:

    for statement in statements:
        res = eval(statement)

        if isinstance(res, ReturnObj):
            return res.value
        
        if isinstance(res, ErrorObj):
            return res

    return res

def eval_block_statements(statements: list[Statement]) -> Object:
    for statement in statements:
        res = eval(statement)

        if isinstance(res, ReturnObj) or isinstance(res, ErrorObj):
            return res

    return res

def eval_prefix_expression(operator: str, right: Object) -> Object:

    if is_eror(right):
        return right

    if operator == '!':
        return eval_bang_operator(right)
    
    elif operator == '-':
        return eval_minus_operator(right)
    
    return ErrorObj(f'unknown operator: {operator}{right.get_type()}')

def eval_minus_operator(right: Object) -> Object:

    if is_eror(right):
        return right

    if isinstance(right, IntegerObj):
        return IntegerObj(-right.value)
    
    return ErrorObj(f'unknown operator: -{right.get_type()}')

def eval_bang_operator(right: Object) -> Object:
    
    if is_eror(right):
        return right

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
    
    return ErrorObj(f'unknown operator: !{right.get_type()}')

def eval_infix_expression(operator: str, left: Object, right: Object) -> Object:
    if operator in ['+', '-', '*', '/', '>', '<', '!=', '==']:

        if is_eror(left):
            return left
        
        if is_eror(right):
            return right

        # handle non integer cases
        if type(left) != type(right):
            return ErrorObj(f'type mismatch: {left.get_type()} {operator} {right.get_type()}')

        if not (isinstance(left, IntegerObj) and isinstance(right, IntegerObj)):
            return ErrorObj(f'unknown operator: {left.get_type()} {operator} {right.get_type()}')
        
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
        
        if operator == '==':
            return BooleanObj(left.value == right.value)
        
        if operator == '!=':
            return BooleanObj(left.value != right.value)
    
    return EvalConstants.NULL_OBJ


def eval_if_expression(exp: IfExpression):
    condition = eval(exp.condition)

    if is_eror(condition):
        return condition

    truthy = is_truthy(condition)
    if is_eror(truthy):
        return truthy

    if condition.value:
        return eval(exp.consequence)
    elif exp.alternative:
        return eval(exp.alternative)

    return EvalConstants.NULL_OBJ


def is_truthy(obj: Object):
    if isinstance(obj, NullObj):
        return EvalConstants.FALSE_BOOLEAN_OBJ
    if isinstance(obj, BooleanObj):
        return obj
    if isinstance(obj, IntegerObj):
        if obj.value > 0:
            return EvalConstants.TRUE_BOOLEAN_OBJ
        return EvalConstants.FALSE_BOOLEAN_OBJ
    
    return ErrorObj('truth value cannont be extracted')


def is_eror(err: Object) -> bool:
    return err and isinstance(err, ErrorObj)