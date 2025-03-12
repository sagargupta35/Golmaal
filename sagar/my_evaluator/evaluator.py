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