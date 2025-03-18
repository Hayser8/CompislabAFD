from symbol import Symbol, SymbolType
import re

class Node:
    pass

class Literal(Node):
    def __init__(self, value, escaped=False):
        self.value = value
        self.escaped = escaped  
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
            self.consume()  
            right = self.parse_term()
            node = Alternation(node, right)
        return node
    
    def parse_term(self):
        node = self.parse_factor()
        while self.current() is not None and self.current() not in {')', '}', '|'}:
            if self.current() == '·':
                self.consume()  
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
        
        # NUEVA RAMA: Manejo de literales en formato LIT<...>
        if self.input.startswith("LIT<<", self.pos):
            end_index = self.input.find(">>", self.pos)
            if end_index == -1:
                raise ValueError("No se encontró '>>' para LIT<< en posición " + str(self.pos))
            literal_content = self.input[self.pos+5:end_index]
            self.pos = end_index + 2
            # Usar regex para detectar si el literal está en formato robusto (comienza con dígitos, luego ':' y luego el contenido)
            robust_match = re.match(r'^(\d+):(.*)$', literal_content)
            if robust_match:
                length_str, content = robust_match.groups()
                try:
                    expected_length = int(length_str)
                except ValueError:
                    raise ValueError("La longitud del literal no es un entero válido en la posición " + str(self.pos))
                if len(content) != expected_length:
                    raise ValueError("La longitud declarada no coincide con la cantidad de caracteres en el literal")
                return Literal(content, escaped=True)
            else:
                # Si no coincide con el formato robusto, se usa el formato antiguo
                return Literal(literal_content, escaped=True)
        
        # Manejo de literales en formato lit(...)
        if self.input.startswith("lit(", self.pos):
            end_index = self.input.find(")", self.pos)
            if end_index == -1:
                raise ValueError("No se encontró ')' para lit( en posición " + str(self.pos))
            literal_content = self.input[self.pos+4:end_index]
            self.pos = end_index + 1
            return Literal(literal_content, escaped=True)
        
        # Manejo de secuencias especiales ya convertidas (por ejemplo, \n, \t, \r)
        if ch in {"\n", "\t", "\r"}:
            self.consume()
            return Literal(ch, escaped=True)
        
        if ch == '(':
            self.consume()  
            node = self.parse_expression()
            if self.current() != ')':
                raise ValueError("Expected ')' at position " + str(self.pos))
            self.consume()  
            return Group(node)
        
        if ch == '{':
            self.consume()  
            node = self.parse_expression()
            if self.current() != '}':
                raise ValueError("Expected '}' at position " + str(self.pos))
            self.consume()  
            return Group(node)
        
        if ch in {'·', '|', '*', '+', '?'}:
            raise ValueError(f"Unexpected operator '{ch}' at position {self.pos}")
        
        # Caso de carácter suelto
        return Literal(self.consume())

    
    @staticmethod
    def is_valid_factor_start(ch):
        return ch not in {'*', '+', '?', '|', '·', ')', '}'}

def parse_regex(input_str):
    parser = Parser(input_str)
    ast = parser.parse_expression()
    if parser.pos != parser.length:
        raise ValueError("Extra characters at end of input")
    return ast

def flatten_concat(node):
    result = []
    stack = []
    current = node
    while stack or current:
        if current:
            if isinstance(current, Concat):
                stack.append(current)
                current = current.left
            else:
                result.append(current)
                current = None
        else:
            current = stack.pop()
            current = current.right
    return result

def escape_for_token(s):
    """
    Escapa caracteres especiales para la representación del literal.
    """
    s = s.replace("\\", "\\\\")
    s = s.replace("\t", "\\t")
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    return s

def to_postfix(node):
    """
    Convierte el AST a notación postfix en forma de cadena.
    Los literales se muestran en el formato LIT<<...>>.
    """
    if isinstance(node, Literal):
        if hasattr(node, 'escaped') and node.escaped:
            content = escape_for_token(node.value)
            length = len(content)
            return f"LIT<<{length}:{content}>>"
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
            return " ".join(parts) + " " + " ".join("·" for _ in range(len(operands) - 1))
        else:
            return parts[0]
    elif isinstance(node, Group):
        return to_postfix(node.child)
    else:
        raise ValueError("Unknown node type in conversion")
