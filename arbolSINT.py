from graphviz import Digraph
from symbol import Symbol

EOF_SYMBOL = '☒'

class TreeNode:
    def __init__(self, value, left=None, right=None):
        """
        Cada nodo tiene:
          - value: el símbolo (operador o literal)
          - left: hijo izquierdo (para operadores unarios o binarios)
          - right: hijo derecho (solo para operadores binarios)
        """
        self.value = value
        self.left = left
        self.right = right

class SyntaxTree:
    def __init__(self, tokens):
        """
        Construye el árbol sintáctico a partir de la lista de tokens en notación postfix.
        Al final se concatena el árbol resultante con un nodo EOF.
        """
        self.tokens = tokens
        tree = self._build_tree(tokens)
        eof_node = TreeNode(EOF_SYMBOL)
        self.root = TreeNode('·', tree, eof_node)

    def _build_tree(self, tokens):
        """
        Usa el algoritmo de pila para convertir la expresión en postfix en un árbol.
        Se asume que los operadores son:
          - Unario: '*' 
          - Binarios: '·' y '|'
        """
        stack = []
        for token in tokens:
            if token.type == "operand":
                node = TreeNode(token.name)
                stack.append(node)
            elif token.type == "operator":
                if token.name == '*':
                    if not stack:
                        raise Exception("Falta operando para '*'")
                    child = stack.pop()
                    node = TreeNode('*', left=child)
                elif token.name in {'·', '|'}:
                    if len(stack) < 2:
                        raise Exception(f"Faltan operandos para '{token.name}'")
                    right = stack.pop()
                    left = stack.pop()
                    node = TreeNode(token.name, left, right)
                else:
                    raise Exception("Operador no soportado: " + token.name)
                stack.append(node)
            else:
                raise Exception("Tipo de token desconocido: " + token.type)
        if len(stack) != 1:
            raise Exception("Expresión postfix inválida, la pila debe quedar con un solo elemento")
        return stack.pop()

    def visualize(self, filename='syntax_tree'):
        """
        Genera la imagen del árbol sintáctico usando Graphviz.
        Se crea un archivo (por ejemplo, syntax_tree.png).
        """
        dot = Digraph(comment='Árbol Sintáctico')
        self._add_nodes(dot, self.root, counter=[0])
        dot.render(filename, format='png', cleanup=True)
        print(f"Imagen del árbol generada: {filename}.png")

    def _add_nodes(self, dot, node, counter):
        """
        Función recursiva que:
          - Crea un nodo en el grafo con un id único.
          - Recorre los hijos y crea las aristas correspondientes.
        Retorna el id (en forma de cadena) del nodo actual.
        """
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
