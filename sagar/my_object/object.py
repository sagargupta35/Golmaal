from __future__ import annotations 
from abc import ABC, abstractmethod
from dataclasses import dataclass
from sagar.my_ast.ast import Identifier, BlockStatement

ObjectType = str

class Object(ABC):

    @abstractmethod
    def get_type(self) -> ObjectType:
        pass
    
    @abstractmethod
    def inspect(self) -> str:
        pass

@dataclass(frozen=True)
class ObjConstants:
    INTEGER_OBJ = 'INTEGER'
    BOOLEAN_OBJ = 'BOOLEAN'
    NULL_OBJ = 'NULL'
    RETURN_VALUE_OBJ = 'RETURN_VALUE'
    ERROR_OBJ = 'ERROR'
    FUNCTION_OBJ = 'FUNCTION'
    STRING_OBJ = 'STRING'

class IntegerObj(Object):
    def __init__(self, value: int):
        self.value: int = value

    def get_type(self):
        return ObjConstants.INTEGER_OBJ
    
    def inspect(self):
        return f"{self.value}"
    
    def __str__(self):
        return self.inspect()

class BooleanObj(Object):

    def __init__(self, value: bool):
        self.value: bool = value

    def get_type(self):
        return ObjConstants.BOOLEAN_OBJ
    
    def inspect(self):
        return f"{self.value}"

    def __str__(self):
        return self.inspect()
    
class NullObj(Object):

    def get_type(self):
        return ObjConstants.NULL_OBJ
    
    def inspect(self):
        return 'NULL'
    

class ReturnObj(Object):

    def __init__(self, value: Object):
        self.value: Object = value

    def get_type(self):
        return ObjConstants.RETURN_VALUE_OBJ

    def inspect(self):
        return self.value.inspect()

class ErrorObj(Object):
    def __init__(self, message: str = ''):
        self.message = message

    def get_type(self):
        return ObjConstants.ERROR_OBJ
    
    def inspect(self):
        return f'Error: {self.message}'
    
class Environment:
    def __init__(self, outer: Environment | None = None):
        self.store = {}
        self.outer = outer

    @classmethod
    def new_enclosing_environment(cls, env: Environment):
        return cls(outer = env)

    def get(self, name):

        if name in self.store:
            return self.store[name]

        if self.outer:
            return self.outer.get(name)
        
        return None

    def put(self, name, val):
        self.store[name] = val
        return val
    
class FunctionObj(Object):
    def __init__(self, params: list[Identifier], body: BlockStatement, env: Environment):
        self.params = params
        self.body = body
        self.env = env

    def get_type(self):
        return ObjConstants.FUNCTION_OBJ
    
    def inspect(self):
        res = [
            'fn',
            '(',
            ', '.join(list(map(str, self.params))),
            ')',
            '{',
            str(self.body),
            '}'
        ]
        return ' '.join(res)

    def __str__(self):
        return self.inspect()
        

class StringObj(Object):
    def __init__(self, value: str):
        self.value = value
    
    def get_type(self):
        return ObjConstants.STRING_OBJ
    
    def inspect(self):
        return f'"{self.value}"'

        