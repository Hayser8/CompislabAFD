import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from symbol import Symbol
import unittest

class TestSymbol(unittest.TestCase):

    def test_symbol_creation(self):
        """Verifica que un símbolo se crea correctamente con el nombre y tipo adecuados."""
        sym = Symbol("a", "operand")
        self.assertEqual(sym.name, "a")
        self.assertEqual(sym.type, "operand")

    def test_symbol_representation(self):
        """Verifica que la representación (__repr__) del símbolo es su nombre."""
        sym = Symbol("b", "operand")
        self.assertEqual(repr(sym), "b")

if __name__ == "__main__":
    unittest.main()
