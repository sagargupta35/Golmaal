from sagar.my_ast.ast import *
from sagar.my_object.object import *
from dataclasses import dataclass

@dataclass(frozen=True)
class EvalConstants:
    TRUE_BOOLEAN_OBJ = BooleanObj(True)
    FALSE_BOOLEAN_OBJ = BooleanObj(False)


def eval(node: Node) -> Object:
    res = NullObj()
    
    if isinstance(node, Program):
        res = eval_statements(node.statements)
    
    elif isinstance(node, ExpressionStatement):
        res = eval(node.expression)

    elif isinstance(node, IntegerLiteral):
        res = IntegerObj(value=node.value)

    elif isinstance(node, Boolean):
        if node.value:
            res = EvalConstants.TRUE_BOOLEAN_OBJ # As all boolean true objs are same follow singleton approach
        else:
            res = EvalConstants.FALSE_BOOLEAN_OBJ
    
    elif isinstance(node, PrefixExpression):
        right = eval(node.right)
        res = eval_prefix_expression(node.operator, right)
    
    if isinstance(res, NullObj):
        res.messages.append('eval')

    return res


def eval_statements(statements: list[Statement]) -> Object:
    res = NullObj()

    for statement in statements:
        res = eval(statement)

    if isinstance(res, NullObj):
        res.messages.append('eval_statements')

    return res

def eval_prefix_expression(operator: str, right: Object) -> Object:
    res = NullObj()

    if operator == '!':
        res = eval_bang_operator(right)
    
    elif operator == '-':
        res = eval_minus_operator(right)
    
    if isinstance(res, NullObj):
        res.messages.append('eval_prefix_expression')
    
    return res

def eval_minus_operator(right: Object) -> Object:
    res = NullObj()

    if isinstance(right, IntegerObj):
        res = IntegerObj(-right.value)
    
    if isinstance(res, NullObj):
        res.messages.append('eval_minus_operator')
    
    return res

def eval_bang_operator(right: Object) -> Object:
    res = NullObj()

    if isinstance(right, BooleanObj):
        if right is EvalConstants.TRUE_BOOLEAN_OBJ:
            res = EvalConstants.FALSE_BOOLEAN_OBJ
        else:
            res = EvalConstants.TRUE_BOOLEAN_OBJ
    elif isinstance(right, IntegerObj):
        if right.value > 0:
            res = EvalConstants.FALSE_BOOLEAN_OBJ
        else:
            res = EvalConstants.TRUE_BOOLEAN_OBJ
    elif isinstance(right, NullObj):
        res = EvalConstants.TRUE_BOOLEAN_OBJ


    if isinstance(res, NullObj):
        res.messages.append('eval_bang_operator')
    
    return res

