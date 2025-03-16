from sagar.my_ast.ast import *
from sagar.my_object.object import *
from dataclasses import dataclass

@dataclass(frozen=True)
class EvalConstants:
    TRUE_BOOLEAN_OBJ = BooleanObj(True)
    FALSE_BOOLEAN_OBJ = BooleanObj(False)
    NULL_OBJ = NullObj()



def eval(node: Node, env: Environment) -> Object:
    
    if isinstance(node, Program):
        return eval_statements(node.statements, env)
    
    elif isinstance(node, ExpressionStatement):
        return eval(node.expression, env)

    elif isinstance(node, IntegerLiteral):
        return IntegerObj(value=node.value)

    elif isinstance(node, Boolean):
        if node.value:
            return EvalConstants.TRUE_BOOLEAN_OBJ # As all boolean true objs are same follow singleton approach
        else:
            return EvalConstants.FALSE_BOOLEAN_OBJ
    
    elif isinstance(node, PrefixExpression):
        right = eval(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    
    elif isinstance(node, InfixExpression):
        left = eval(node.left, env)
        if is_error(left):
            return left
        right = eval(node.right, env)
        if is_error(right):
            return right
        return eval_infix_expression(node.operator, left, right)

    elif isinstance(node, BlockStatement):
        return eval_block_statements(node.statements, env)
    
    elif isinstance(node, IfExpression):
        return eval_if_expression(node, env)
    
    elif isinstance(node, ReturnStatement):
        value = eval(node.value, env)
        if is_error(value):
            return value
        return ReturnObj(value=value)
    
    elif isinstance(node, LetStatement):
        value = eval(node.value, env)
        if is_error(value):
            return value
        env.put(node.name.value, value)
        return NullObj()

    elif isinstance(node, Identifier):        
        return eval_identifier(node.value, env)
    
    elif isinstance(node, FunctionLiteral):
        return FunctionObj(params=node.parameters, body=node.body, env=env)
    
    elif isinstance(node, CallExpression):
        fun = eval(node.function, env)
        if is_error(fun):
            return fun
        args = eval_arguments(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args
        return apply_fun(fun, args)
    
    elif isinstance(node, StringExpression):
        str_obj = StringObj(node.value)
        return str_obj
          
    return ErrorObj('cannot evaluate the statement')


def apply_fun(fun: Object, args: list[Object]) -> Object:

    if not isinstance(fun, FunctionObj):
        return ErrorObj(f'not a function: {str(fun)}')

    extended_env = get_extended_env(fun, args)

    if is_error(extended_env):
        return extended_env
    
    evaluated = eval_block_statements(fun.body.statements, env = extended_env)

    return unwrap_return_value(evaluated)
    

def get_extended_env(fun: FunctionObj, args: list[Object]):
    extended_env = Environment.new_enclosing_environment(fun.env)
    
    if len(fun.params) != len(args):
        return ErrorObj(f'expected {len(fun.params)} arguments. but passed {len(args)}.')

    for i, param in enumerate(fun.params):
        extended_env.put(param.value, args[i])

    return extended_env
    
def unwrap_return_value(ret: Object) -> Object:
    if not isinstance(ret, ReturnObj):
        return ret
    
    return ret.value


def eval_arguments(args: list[Expression], env: Environment) -> list[Object]:
    res = []
    for arg in args:
        evaluated = eval(arg, env)
        if is_error(evaluated):
            return [evaluated]
        res.append(evaluated)
    return res


def eval_statements(statements: list[Statement], env: Environment) -> Object:
    for statement in statements:
        res = eval(statement, env)

        if isinstance(res, ReturnObj):
            return res.value
        
        if isinstance(res, ErrorObj):
            return res

    return res

def eval_block_statements(statements: list[Statement], env: Environment) -> Object:

    for statement in statements:
        res = eval(statement, env)

        if isinstance(res, ReturnObj) or isinstance(res, ErrorObj):
            return res

    return res

def eval_prefix_expression(operator: str, right: Object) -> Object:

    if is_error(right):
        return right

    if operator == '!':
        return eval_bang_operator(right)
    
    elif operator == '-':
        return eval_minus_operator(right)
    
    return ErrorObj(f'unknown operator: {operator}{right.get_type()}')

def eval_minus_operator(right: Object) -> Object:

    if is_error(right):
        return right

    if isinstance(right, IntegerObj):
        return IntegerObj(-right.value)
    
    return ErrorObj(f'unknown operator: -{right.get_type()}')

def eval_bang_operator(right: Object) -> Object:
    
    if is_error(right):
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

        if is_error(left):
            return left
        
        if is_error(right):
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


def eval_if_expression(exp: IfExpression, env: Environment):
    condition = eval(exp.condition, env)

    if is_error(condition):
        return condition

    truthy = is_truthy(condition)
    if is_error(truthy):
        return truthy

    if condition.value:
        return eval(exp.consequence, env)
    elif exp.alternative:
        return eval(exp.alternative, env)

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

def eval_identifier(name, env: Environment):
    res = env.get(name)
    if res:
        return res
    return ErrorObj(f'identifier not found: {name}')

def is_error(err: Object) -> bool:
    return err and isinstance(err, ErrorObj)