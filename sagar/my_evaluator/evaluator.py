from sagar.my_ast.ast import *
from sagar.my_object.object import *
from dataclasses import dataclass

@dataclass(frozen=True)
class EvalConstants:
    TRUE_BOOLEAN_OBJ = BooleanObj(True)
    FALSE_BOOLEAN_OBJ = BooleanObj(False)
    NULL_OBJ = NullObj()


def __length(args: list[Object], **kwargs) -> Object:
    if len(args) != 1:
        return ErrorObj(f"wrong number of arguments. got={len(args)}, want=1")
    arg: Object = args[0]
    if isinstance(arg, StringObj):
        return IntegerObj(len(arg.value))
    elif isinstance(arg, ArrayObj):
        return IntegerObj(len(arg.elements))
    return ErrorObj(f"argument to 'len' not supported, got {arg.get_type()}")

def __print(args: list[Object], **kwargs) -> NullObj | ErrorObj:
    env = kwargs['env']
    if not env:
        return ErrorObj('no environment found to print')
    if not isinstance(env, Environment):
        return ErrorObj('no environment found to print')
    res = []
    for obj in args:
        res.append(str(obj))
    res = ''.join(res)
    overload = env.print(res)
    if overload:
        return ErrorObj('Cannot print more than 1000 statements currently.')
    return NullObj()

builtins = {
    'len': Builtin(__length, name = 'len'),
    'print': Builtin(__print, name = 'print'),
    'break': BuiltinKeywordFunction(name='break'),
    'continue': BuiltinKeywordFunction(name = 'continue')
}


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
        if node.name.value in builtins:
            return ErrorObj(f'cannot override builtin function: {node.name.value}')
        if not isinstance(node.value, Expression):
            return ErrorObj(f'not an expression: {node.value.token_literal()}')
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
        return apply_fun(fun, node.arguments, env)
    
    elif isinstance(node, StringExpression):
        str_obj = StringObj(node.value)
        return str_obj
    
    elif isinstance(node, ArrayLiteral):
        elements = eval_arguments(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]
        arr_obj = ArrayObj(elements=elements)
        return arr_obj
    
    elif isinstance(node, AssignmentStatement):
        right = eval(node.right, env)
        if is_error(right):
            return right
        ass_obj = AssignmentObj(node.left, right)
        evaluated = eval_assignment(ass_obj, env)
        return evaluated

    elif isinstance(node, WhileStatement):
        return eval_while_statement(node, env)

    elif isinstance(node, IndexExpression):
        return eval_index_operation(node, env)
          
    return ErrorObj('cannot evaluate the statement')


def apply_fun(fun: Object, raw_args: list[Expression], env: Environment) -> Object:
    args = eval_arguments(raw_args, env)

    if len(args) == 1 and is_error(args[0]):
        return args[0]

    if isinstance(fun, FunctionObj):
        extended_env = get_extended_env(fun, args)
        if is_error(extended_env):
            return extended_env
        evaluated = eval_block_statements(fun.body.statements, env = extended_env)
        return unwrap_return_value(evaluated)
    
    elif isinstance(fun, Builtin):
        return fun.fn(args, env = env)
     
    return ErrorObj(f'not a function: {str(fun)}')
    

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
        
        if isinstance(left, StringObj) or isinstance(right, StringObj):
            return StringObj(value=str(left) + str(right))

        # handle non integer cases
        if type(left) != type(right):
            return ErrorObj(f'type mismatch: {left.get_type()} {operator} {right.get_type()}')
        
        #concatenate string
        if isinstance(left, StringObj) and isinstance(right, StringObj) and operator == '+':
            return StringObj(value=left.value + right.value)

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

    truthy = get_truthy(condition)
    if is_error(truthy):
        return truthy

    if condition.value:
        return eval(exp.consequence, env)
    elif exp.alternative:
        return eval(exp.alternative, env)

    return EvalConstants.NULL_OBJ


def eval_while_statement(whl_stmt: WhileStatement, env: Environment) -> NullObj | ErrorObj:
    condition = eval(whl_stmt.condition, env)

    if is_error(condition):
        return condition

    truthy = get_truthy(condition)
    if is_error(truthy):
        return truthy

    iter_left = 1000

    while truthy.value:
        if iter_left == 0:
            return ErrorObj('Can only perform 1000 iterations currently')
        res = EvalConstants.NULL_OBJ
        for stmt in whl_stmt.body.statements:
            res = eval(stmt, env)
            if is_error(res):
                return res
            if isinstance(res, ReturnObj):
                return ErrorObj('cannot have a return statement inside a while function')
            if isinstance(res, BuiltinKeywordFunction):
                break
        
        if isinstance(res, BuiltinKeywordFunction) and res.name == 'break':
            break
        
        condition = eval(whl_stmt.condition, env)
        if is_error(condition):
            return condition
        truthy = get_truthy(condition)
        if is_error(truthy):
            return truthy
        iter_left = iter_left-1
    return EvalConstants.NULL_OBJ


def get_truthy(obj: Object) -> BooleanObj | ErrorObj:
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
    res = builtins.get(name, None)
    if res:
        return res
    return ErrorObj(f'identifier not found: {name}')

def eval_assignment(obj: AssignmentObj, env: Environment):
    if isinstance(obj.left, Identifier):
        iden: Identifier = obj.left
        prev = env.get(iden.value)
        if not prev:
            return ErrorObj(f'identifier not declared: {iden.value}')
        env.put(iden.value, obj.right)
        return EvalConstants.NULL_OBJ

    return ErrorObj(f'cannot assign value to {obj.inspect()}')

def eval_index_operation(ie: IndexExpression, env: Environment):
    arr = eval(ie.left, env)
    if is_error(arr):
        return arr
    if not isinstance(arr, ArrayObj):
        return ErrorObj(f'{arr.get_type()} cannot be subscripted')
    index: Object = eval(ie.index, env)
    if is_error(index):
        return index
    if not isinstance(index, IntegerObj):
        return ErrorObj(f'cannot index an array with non-integer types: {index.get_type()}')
    elements = arr.elements
    if index.value < 0 or index.value >= len(elements):
        return ErrorObj(f'Array index out of bounds for length {len(elements)}: {index.value}')
    return elements[index.value]

def is_error(err: Object) -> bool:
    return err and isinstance(err, ErrorObj)