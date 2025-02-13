import unittest
from arbolSINT import SyntaxTree, TreeNode
from symbol import Symbol

class TestSyntaxTree(unittest.TestCase):
    def test_tree_construction(self):
        # Creamos tokens para la notación postfix de "a b ·"
        tokens = [
            Symbol("a", "operand"),
            Symbol("b", "operand"),
            Symbol("·", "operator")
        ]
        st = SyntaxTree(tokens)
        # El árbol sintáctico se construye concatenando el árbol obtenido
        # con un nodo EOF (☒). Así, la raíz es un nodo "·" con dos hijos.
        self.assertEqual(st.root.value, "·")
        # El hijo izquierdo es el árbol obtenido de _build_tree (debe ser "·")
        self.assertEqual(st.root.left.value, "·")
        # Los hijos de ese nodo son los literales "a" y "b"
        self.assertEqual(st.root.left.left.value, "a")
        self.assertEqual(st.root.left.right.value, "b")
        # El hijo derecho de la raíz es el nodo EOF
        self.assertEqual(st.root.right.value, "☒")

if __name__ == '__main__':
    unittest.main()
