# parser.py
from symbol import Symbol

# Nodos del AST
class Node:
    pass

class Literal(Node):
    def __init__(self, value, escaped=False):
        self.value = value
        self.escaped = escaped  # Indica si el literal proviene de un escape
    def __repr__(self):
        return self.value

class Concat(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Concat({self.left},{self.right})"

class Alternation(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Alt({self.left},{self.right})"

class Star(Node):
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return f"Star({self.child})"

class Epsilon(Node):
    def __init__(self):
        self.value = "ε"
    def __repr__(self):
        return self.value

class Plus(Node):
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return f"Plus({self.child})"

class Group(Node):
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return f"Group({self.child})"

class Parser:
    def __init__(self, input_str):
        self.input = input_str
        self.pos = 0
        self.length = len(input_str)
    
    def current(self):
        if self.pos < self.length:
            return self.input[self.pos]
        return None
    
    def consume(self):
        ch = self.current()
        self.pos += 1
        return ch
    
    def parse_expression(self):
        node = self.parse_term()
        while self.current() == '|':
            self.consume()  # consume '|'
            right = self.parse_term()
            node = Alternation(node, right)
        return node
    
    def parse_term(self):
        node = self.parse_factor()
        while self.current() is not None and self.current() not in {')', '}', '|'}:
            if self.current() == '·':
                self.consume()  # consume '·'
                if self.current() is None or not Parser.is_valid_factor_start(self.current()):
                    raise ValueError("Expected factor after concatenation operator")
                right = self.parse_factor()
                node = Concat(node, right)
            elif Parser.is_valid_factor_start(self.current()):
                right = self.parse_factor()
                node = Concat(node, right)
            else:
                break
        return node
    
    def parse_factor(self):
        node = self.parse_base()
        while self.current() in ['*', '+', '?']:
            op = self.consume()
            if op == '*':
                node = Star(node)
            elif op == '+':
                node = Plus(node)
            elif op == '?':
                node = Alternation(node, Epsilon())
        return node
    
    def parse_base(self):
        ch = self.current()
        if ch is None:
            raise ValueError("Unexpected end of input in parse_base")
        if ch == '§':
            self.consume()  # consume el marcador de escape
            next_ch = self.consume()
            # Se elimina el icono '§' y se retorna solo el carácter escapado
            return Literal(next_ch, escaped=True)
        if ch == '(':
            self.consume()  # consume '('
            node = self.parse_expression()
            if self.current() != ')':
                raise ValueError("Expected ')' at position " + str(self.pos))
            self.consume()  # consume ')'
            return Group(node)
        if ch == '{':
            self.consume()  # consume '{'
            node = self.parse_expression()
            if self.current() != '}':
                raise ValueError("Expected '}' at position " + str(self.pos))
            self.consume()  # consume '}'
            return Group(node)
        if ch in {'·', '|', '*', '+', '?'}:
            raise ValueError(f"Unexpected operator '{ch}' at position {self.pos}")
        return Literal(self.consume())
    
    @staticmethod
    def is_valid_factor_start(ch):
        # Un carácter es válido para iniciar un factor si no es un operador o delimitador de cierre.
        return ch not in {'*', '+', '?', '|', '·', ')', '}'}

def parse_regex(input_str):
    parser = Parser(input_str)
    ast = parser.parse_expression()
    if parser.pos != parser.length:
        raise ValueError("Extra characters at end of input")
    return ast

def flatten_concat(node):
    if isinstance(node, Concat):
        return flatten_concat(node.left) + flatten_concat(node.right)
    else:
        return [node]

def to_postfix(node):
    """
    Convierte el AST a notación postfix.
    Para un nodo de concatenación con N operandos se generan N-1 operadores '·'.
    """
    if isinstance(node, Literal):
        if hasattr(node, 'escaped') and node.escaped:
            return f"lit({node.value})"
        return node.value
    elif isinstance(node, Epsilon):
        return "ε"
    elif isinstance(node, Star):
        return to_postfix(node.child) + " *"
    elif isinstance(node, Plus):
        base = to_postfix(node.child)
        star = to_postfix(Star(node.child))
        return base + " " + star + " ·"
    elif isinstance(node, Alternation):
        return to_postfix(node.left) + " " + to_postfix(node.right) + " |"
    elif isinstance(node, Concat):
        operands = flatten_concat(node)
        parts = [to_postfix(op) for op in operands]
        if len(operands) > 1:
            # Para N operandos se necesitan N-1 operadores de concatenación
            return " ".join(parts) + " " + " ".join("·" for _ in range(len(operands)-1))
        else:
            return parts[0]
    elif isinstance(node, Group):
        return to_postfix(node.child)
    else:
        raise ValueError("Unknown node type in conversion")
