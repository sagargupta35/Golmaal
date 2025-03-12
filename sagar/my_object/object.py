from abc import ABC, abstractmethod
from dataclasses import dataclass

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

class IntegerObj(Object):
    def __init__(self, value: int):
        self.value: int = value

    def get_type(self):
        return ObjConstants.INTEGER_OBJ
    
    def inspect(self):
        return f"{self.value}"

class BooleanObj(Object):

    def __init__(self, value: bool):
        self.value: bool = value

    def get_type(self):
        return ObjConstants.BOOLEAN_OBJ
    
    def inspect(self):
        return f"{self.value}"
    
class NullObj(Object):

    def __init__(self):
        self.messages = []

    def __str__(self):
        res = ['NullObj:']
        for message in self.messages:
            res.append(f'{message} ->')
        return ' '.join(res)

    def get_type(self):
        return ObjConstants.NULL_OBJ
    
    def inspect(self):
        return str(self)