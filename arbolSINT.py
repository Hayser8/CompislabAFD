from symbol import Symbol

class SyntaxNode:
    """
    Nodo del árbol sintáctico para la construcción del DFA.
    Cada nodo tiene un símbolo; los nodos hoja (operandos) reciben una posición única.
    """
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol      
        self.left = left
        self.right = right
        self.nullable = False 
        self.firstpos = set() 
        self.lastpos = set()  
        self.position = None  # Solo para hojas (operandos)

    def __repr__(self):
        if self.position is not None:
            return f"({self.symbol}, pos={self.position})"
        else:
            return f"({self.symbol})"

class SyntaxTree:
    """
    Construye el árbol sintáctico a partir de una lista (postfix) de objetos Symbol.
    Se agrega un marcador de fin (#) mediante la concatenación al final.
    Luego se calculan nullable, firstpos, lastpos y followpos.
    """
    def __init__(self, postfix_tokens):
        # Se agrega el símbolo de fin de cadena (#) al final, concatenándolo con el operador de concatenación "·"
        self.postfix_tokens = postfix_tokens + [Symbol('#', 'operand'), Symbol('·', 'operator')]
        print("Postfix tokens for SyntaxTree:", self.postfix_tokens)
        self.root = self.build_tree()
        print("Syntax Tree Root:", self.root)
        self.followpos = {}
        self.assign_positions()
        self.compute_nullable_first_last()
        self.compute_followpos()

    def build_tree(self):
        stack = []
        for token in self.postfix_tokens:
            if token.type == "operand":
                node = SyntaxNode(token)
                stack.append(node)
            elif token.type == "operator":
                if token.name in {'*', '?', '+'}:
                    if not stack:
                        raise ValueError("pop from empty list during unary operator processing")
                    child = stack.pop()
                    node = SyntaxNode(token, left=child)
                else:  # operadores binarios: concatenación ('·') y alternación ('|')
                    if len(stack) < 2:
                        raise ValueError("pop from empty list during binary operator processing")
                    right = stack.pop()
                    left = stack.pop()
                    node = SyntaxNode(token, left, right)
                stack.append(node)
        if not stack:
            raise ValueError("Empty stack after building syntax tree")
        return stack.pop()

    def assign_positions(self):
        self._next_pos = 1
        def traverse(node):
            if node is None:
                return
            traverse(node.left)
            traverse(node.right)
            if node.symbol.type == "operand" and node.symbol.name != 'ε':
                node.position = self._next_pos
                self._next_pos += 1
        traverse(self.root)
        print("Assigned positions in Syntax Tree.")

    def compute_nullable_first_last(self):
        def traverse(node):
            if node is None:
                return
            traverse(node.left)
            traverse(node.right)
            if node.symbol.type == "operand":
                node.nullable = False
                if node.position is not None:
                    node.firstpos.add(node)
                    node.lastpos.add(node)
            elif node.symbol.name == '|':
                node.nullable = node.left.nullable or node.right.nullable
                node.firstpos = node.left.firstpos.union(node.right.firstpos)
                node.lastpos = node.left.lastpos.union(node.right.lastpos)
            elif node.symbol.name == '·':
                node.nullable = node.left.nullable and node.right.nullable
                if node.left.nullable:
                    node.firstpos = node.left.firstpos.union(node.right.firstpos)
                else:
                    node.firstpos = set(node.left.firstpos)
                if node.right.nullable:
                    node.lastpos = node.left.lastpos.union(node.right.lastpos)
                else:
                    node.lastpos = set(node.right.lastpos)
            elif node.symbol.name == '*':
                node.nullable = True
                node.firstpos = set(node.left.firstpos)
                node.lastpos = set(node.left.lastpos)
            elif node.symbol.name == '?':
                node.nullable = True
                node.firstpos = set(node.left.firstpos)
                node.lastpos = set(node.left.lastpos)
            elif node.symbol.name == '+':
                node.nullable = node.left.nullable
                node.firstpos = set(node.left.firstpos)
                node.lastpos = set(node.left.lastpos)
        traverse(self.root)
        print("Computed nullable, firstpos, and lastpos.")

    def compute_followpos(self):
        self.followpos = {}
        def traverse(node):
            if node is None:
                return
            traverse(node.left)
            traverse(node.right)
            if node.symbol.name == '·':
                for n in node.left.lastpos:
                    self.followpos.setdefault(n, set()).update(node.right.firstpos)
            if node.symbol.name in {'*', '+'}:
                for n in node.lastpos:
                    self.followpos.setdefault(n, set()).update(node.firstpos)
        traverse(self.root)
        print("Computed followpos.")
