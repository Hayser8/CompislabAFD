from enum import Enum

class SymbolType(Enum):
    LITERAL = 1
    OPERATOR = 2
    EPSILON = 3
    # Agrega otros tipos si es necesario

class Symbol:
    def __init__(self, value, symbol_type: SymbolType):
        self.value = value
        self.type = symbol_type

    @property
    def name(self):
        return self.value

    def __repr__(self):
        return f"Symbol({self.value!r}, {self.type.name})"
