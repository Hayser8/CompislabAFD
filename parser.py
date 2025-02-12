from symbol import Symbol  
# Nodos del AST
class Node:
    pass

class Literal(Node):
    def __init__(self, value):
        self.value = value
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

# Clase Parser
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
        nodes = []
        # Termina la concatenación al encontrar ')' o '}' o el operador '|'
        while self.current() is not None and self.current() not in [')', '}', '|']:
            nodes.append(self.parse_factor())
        if not nodes:
            return Epsilon()
        node = nodes[0]
        for n in nodes[1:]:
            node = Concat(node, n)
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
        # Si se encuentra el marcador de escape, se consume y se trata el siguiente carácter como literal.
        if ch == '§':
            self.consume()  # consume el marcador
            next_ch = self.consume()
            return Literal(next_ch)
        # Agrupamiento en paréntesis: se consume y se envuelve en un nodo Group.
        if ch == '(':
            self.consume()  # consume '('
            node = self.parse_expression()
            if self.current() != ')':
                raise ValueError("Expected ')' at position " + str(self.pos))
            self.consume()  # consume ')'
            return Group(node)
        # Agrupamiento en llaves: se trata de forma similar.
        if ch == '{':
            self.consume()  # consume '{'
            node = self.parse_expression()
            if self.current() != '}':
                raise ValueError("Expected '}' at position " + str(self.pos))
            self.consume()  # consume '}'
            return Group(node)
        # Cualquier otro carácter se trata como literal.
        return Literal(self.consume())

def parse_regex(input_str):
    parser = Parser(input_str)
    ast = parser.parse_expression()
    if parser.pos != parser.length:
        raise ValueError("Extra characters at end of input")
    return ast

# Función auxiliar para aplanar nodos de concatenación
def flatten_concat(node):
    if isinstance(node, Concat):
        return flatten_concat(node.left) + flatten_concat(node.right)
    else:
        return [node]

# Conversión a postfix sin insertar operadores de concatenación internos.
def to_postfix_no_concat(node):
    if isinstance(node, Literal):
        return node.value
    elif isinstance(node, Epsilon):
        return "ε"
    elif isinstance(node, Star):
        return to_postfix_no_concat(node.child) + " *"
    elif isinstance(node, Alternation):
        return to_postfix_no_concat(node.left) + " " + to_postfix_no_concat(node.right) + " |"
    elif isinstance(node, Concat):
        return " ".join(to_postfix_no_concat(n) for n in flatten_concat(node))
    elif isinstance(node, Plus):
        base = to_postfix_no_concat(node.child)
        star = to_postfix_no_concat(Star(node.child))
        result = base + " " + star + " ."
        if isinstance(node.child, Group):
            if len(base.split()) > 1:
                result += " ."
        return result
    elif isinstance(node, Group):
        return to_postfix_no_concat(node.child)
    else:
        raise ValueError("Unknown node type in no_concat conversion")

# Conversión principal a postfix.
def to_postfix(node):
    if isinstance(node, Group):
        return to_postfix_no_concat(node.child)
    elif isinstance(node, Concat):
        tokens = flatten_concat(node)
        tokens_post = []
        for i, t in enumerate(tokens):
            # Si el token es un Group, usamos la conversión sin concatenación.
            if isinstance(t, Group):
                s = to_postfix_no_concat(t.child)
            else:
                s = to_postfix(t)
            # Si no es el último token y el token no es Plus (que ya incluye el operador),
            # se elimina un operador de concatenación final si está presente.
            if i < len(tokens) - 1:
                if not isinstance(t, Plus) and s.endswith(" ."):
                    s = s[:-2]
            tokens_post.append(s)
        result = " ".join(tokens_post)
        if not result.endswith(" ."):
            result += " ."
        return result
    elif isinstance(node, Alternation):
        return to_postfix(node.left) + " " + to_postfix(node.right) + " |"
    elif isinstance(node, Star):
        return to_postfix(node.child) + " *"
    elif isinstance(node, Plus):
        base = to_postfix(node.child)
        star = to_postfix(Star(node.child))
        result = base + " " + star + " ."
        if isinstance(node.child, Group):
            if len(to_postfix_no_concat(node.child.child).split()) > 1:
                result += " ."
        return result
    elif isinstance(node, Literal):
        return node.value
    elif isinstance(node, Epsilon):
        return "ε"
    else:
        raise ValueError("Unknown node type in conversion")
