from sagar.my_ast.ast import *
from sagar.my_object.object import *
from dataclasses import dataclass

@dataclass(frozen=True)
class EvalConstants:
    TRUE_BOOLEAN_OBJ = BooleanObj(True)
    FALSE_BOOLEAN_OBJ = BooleanObj(False)
    NULL_OBJ = NullObj()


class Evaluator:

    def __init__(self, env: Environment = Environment()):
        self.env = env

    def eval(self, node: Node) -> Object:
        
        if isinstance(node, Program):
            return self.eval_statements(node.statements)
        
        elif isinstance(node, ExpressionStatement):
            return self.eval(node.expression)

        elif isinstance(node, IntegerLiteral):
            return IntegerObj(value=node.value)

        elif isinstance(node, Boolean):
            if node.value:
                return EvalConstants.TRUE_BOOLEAN_OBJ # As all boolean true objs are same follow singleton approach
            else:
                return EvalConstants.FALSE_BOOLEAN_OBJ
        
        elif isinstance(node, PrefixExpression):
            right = self.eval(node.right)
            if self.is_eror(right):
                return right
            return self.eval_prefix_expression(node.operator, right)
        
        elif isinstance(node, InfixExpression):
            left = self.eval(node.left)
            if self.is_eror(left):
                return left
            right = self.eval(node.right)
            if self.is_eror(right):
                return right
            return self.eval_infix_expression(node.operator, left, right)

        elif isinstance(node, BlockStatement):
            return self.eval_block_statements(node.statements)
        
        elif isinstance(node, IfExpression):
            return self.eval_if_expression(node)
        
        elif isinstance(node, ReturnStatement):
            value = self.eval(node.value)
            if self.is_eror(value):
                return value
            return ReturnObj(value=value)
        
        elif isinstance(node, LetStatement):
            value = self.eval(node.value)
            if self.is_eror(value):
                return value
            
        
        return ErrorObj('cannot evaluate the statement')


    def eval_statements(self, statements: list[Statement]) -> Object:

        for statement in statements:
            res = self.eval(statement)

            if isinstance(res, ReturnObj):
                return res.value
            
            if isinstance(res, ErrorObj):
                return res

        return res

    def eval_block_statements(self, statements: list[Statement]) -> Object:
        for statement in statements:
            res = self.eval(statement)

            if isinstance(res, ReturnObj) or isinstance(res, ErrorObj):
                return res

        return res

    def eval_prefix_expression(self, operator: str, right: Object) -> Object:

        if self.is_eror(right):
            return right

        if operator == '!':
            return self.eval_bang_operator(right)
        
        elif operator == '-':
            return self.eval_minus_operator(right)
        
        return ErrorObj(f'unknown operator: {operator}{right.get_type()}')

    def eval_minus_operator(self, right: Object) -> Object:

        if self.is_eror(right):
            return right

        if isinstance(right, IntegerObj):
            return IntegerObj(-right.value)
        
        return ErrorObj(f'unknown operator: -{right.get_type()}')

    def eval_bang_operator(self, right: Object) -> Object:
        
        if self.is_eror(right):
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

    def eval_infix_expression(self, operator: str, left: Object, right: Object) -> Object:
        if operator in ['+', '-', '*', '/', '>', '<', '!=', '==']:

            if self.is_eror(left):
                return left
            
            if self.is_eror(right):
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


    def eval_if_expression(self, exp: IfExpression):
        condition = self.eval(exp.condition)

        if self.is_eror(condition):
            return condition

        truthy = self.is_truthy(condition)
        if self.is_eror(truthy):
            return truthy

        if condition.value:
            return self.eval(exp.consequence)
        elif exp.alternative:
            return self.eval(exp.alternative)

        return EvalConstants.NULL_OBJ


    def is_truthy(self, obj: Object):
        if isinstance(obj, NullObj):
            return EvalConstants.FALSE_BOOLEAN_OBJ
        if isinstance(obj, BooleanObj):
            return obj
        if isinstance(obj, IntegerObj):
            if obj.value > 0:
                return EvalConstants.TRUE_BOOLEAN_OBJ
            return EvalConstants.FALSE_BOOLEAN_OBJ
        
        return ErrorObj('truth value cannont be extracted')


    def is_eror(self, err: Object) -> bool:
        return err and isinstance(err, ErrorObj)