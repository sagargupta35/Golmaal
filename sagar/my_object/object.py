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