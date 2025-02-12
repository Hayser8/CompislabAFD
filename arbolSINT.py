from graphviz import Digraph
import re

class SyntaxNode:
    """
    Nodo del Árbol Sintáctico.
    """
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol  
        self.left = left      
        self.right = right    
        self.nullable = False 
        self.firstpos = set() 
        self.lastpos = set()  

class SyntaxTree:
    """
    Árbol Sintáctico para Expresiones Regulares.
    """
    def __init__(self, postfix_expr):
        self.postfix_expr = postfix_expr  
        self.root = self.build_tree()     
        self.compute_nullable_first_last()
        self.compute_followpos()  

    def build_tree(self):
        """Construye el árbol sintáctico a partir de la notación postfix."""
        stack = []
        
        for symbol in self.postfix_expr:
            if symbol.type == "operand":
                stack.append(SyntaxNode(symbol))
            elif symbol.type == "operator":
                if symbol.name in {'*', '?', '+'}: 
                    node = SyntaxNode(symbol, left=stack.pop())
                else:  
                    right = stack.pop()
                    left = stack.pop()
                    node = SyntaxNode(symbol, left, right)
                stack.append(node)
        
        return stack.pop() if stack else None
    
    def compute_nullable_first_last(self):
        """Calcula nullable, firstpos y lastpos para cada nodo del árbol."""
        def traverse(node):
            if not node:
                return
            
            traverse(node.left)
            traverse(node.right)
            
            if node.symbol.type == "operand":
                node.firstpos.add(node)
                node.lastpos.add(node)
                node.nullable = False
            elif node.symbol.name == '|':
                node.nullable = node.left.nullable or node.right.nullable
                node.firstpos = node.left.firstpos | node.right.firstpos
                node.lastpos = node.left.lastpos | node.right.lastpos
            elif node.symbol.name == '.':
                node.nullable = node.left.nullable and node.right.nullable
                node.firstpos = node.left.firstpos | node.right.firstpos if node.left.nullable else node.left.firstpos
                node.lastpos = node.left.lastpos | node.right.lastpos if node.right.nullable else node.left.lastpos
            elif node.symbol.name == '*':
                node.nullable = True
                node.firstpos = node.left.firstpos
                node.lastpos = node.left.lastpos
            elif node.symbol.name == '?':
                node.nullable = True
                node.firstpos = node.left.firstpos
                node.lastpos = node.left.lastpos
            elif node.symbol.name == '+':
                node.nullable = node.left.nullable
                node.firstpos = node.left.firstpos
                node.lastpos = node.left.lastpos

        traverse(self.root)
    
    def compute_followpos(self):
        """Calcula followpos para cada posición del árbol sintáctico."""
        followpos = {} 

        def traverse(node):
            if not node:
                return
            
            traverse(node.left)
            traverse(node.right)

            if node.symbol.name == '.':
                for last in node.left.lastpos:
                    followpos.setdefault(last, set()).update(node.right.firstpos)
            elif node.symbol.name == '*':
                for last in node.lastpos:
                    followpos.setdefault(last, set()).update(node.firstpos)

        traverse(self.root)
        self.followpos = followpos 
    def visualize(self, filename="syntax_tree"):
        """Genera la visualización del árbol sintáctico con Graphviz."""
        filename = re.sub(r'[^a-zA-Z0-9_]', '_', filename)
        dot = Digraph()
        self._add_nodes(dot, self.root)
        dot.render(filename, format="png", cleanup=True)
    
    def _add_nodes(self, dot, node, counter=[0]):
        """Agrega nodos recursivamente a Graphviz."""
        if node:
            node_id = str(counter[0])
            dot.node(node_id, node.symbol.name)
            counter[0] += 1
            
            if node.left:
                left_id = str(counter[0])
                self._add_nodes(dot, node.left, counter)
                dot.edge(node_id, left_id)
            
            if node.right:
                right_id = str(counter[0])
                self._add_nodes(dot, node.right, counter)
                dot.edge(node_id, right_id)
