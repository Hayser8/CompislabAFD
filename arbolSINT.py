from graphviz import Digraph
from symbol import Symbol, SymbolType

class TreeNode:
    def __init__(self, value, left=None, right=None):
        """
        Nodo del árbol sintáctico:
          - value: símbolo (literal u operador)
          - left, right: hijos
        """
        self.value = value
        self.left = left
        self.right = right

class SyntaxTree:
    def __init__(self, tokens):
        """
        Construye el árbol sintáctico a partir de una lista de tokens en postfix.
        No se añade ningún símbolo extra al final.
        """
        self.tokens = tokens
        self.root = self._build_tree(tokens)

    def _build_tree(self, tokens):
        stack = []
        for token in tokens:
            if token.type == SymbolType.LITERAL:
                stack.append(TreeNode(token.name))
            elif token.type == SymbolType.OPERATOR:
                if token.name == '*':
                    if not stack:
                        raise Exception("Falta operando para '*'")
                    child = stack.pop()
                    stack.append(TreeNode('*', left=child))
                elif token.name in {'·', '|'}:
                    if len(stack) < 2:
                        raise Exception(f"Faltan operandos para '{token.name}'")
                    right = stack.pop()
                    left  = stack.pop()
                    stack.append(TreeNode(token.name, left, right))
                else:
                    raise Exception(f"Operador no soportado: {token.name}")
            else:
                raise Exception(f"Tipo de token desconocido: {token.type}")
        if len(stack) != 1:
            raise Exception("Expresión postfix inválida; la pila debe contener un solo elemento")
        return stack.pop()

    def visualize(self, filename='syntax_tree'):
        dot = Digraph(comment='Árbol Sintáctico')
        self._add_nodes(dot, self.root, counter=[0])
        dot.render(filename, format='png', cleanup=True)
        print(f"Imagen del árbol generada: {filename}.png")

    def _add_nodes(self, dot, node, counter):
        node_id = str(counter[0])
        dot.node(node_id, label=node.value)
        counter[0] += 1
        if node.left:
            left_id = self._add_nodes(dot, node.left, counter)
            dot.edge(node_id, left_id)
        if node.right:
            right_id = self._add_nodes(dot, node.right, counter)
            dot.edge(node_id, right_id)
        return node_id
