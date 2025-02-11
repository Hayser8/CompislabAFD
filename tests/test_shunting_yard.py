import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shunting_yard import shunting_yard
from symbol import Symbol
import unittest

class TestShuntingYard(unittest.TestCase):

    def test_simple_expression(self):
        """
        Prueba la conversión de una expresión simple con concatenación y Kleene (*).
        """
        expr = "a.b*"
        expected_postfix = ["a", "b", "*", "."]
        result = [s.name for s in shunting_yard(expr)]
        self.assertEqual(result, expected_postfix)

    def test_expression_with_union(self):
        """
        Prueba una expresión con unión (|) y concatenación explícita.
        """
        expr = "a|b.c"
        expected_postfix = ["a", "b", "|", "c", "."]
        result = [s.name for s in shunting_yard(expr)]
        print(f"DEBUG: {result}")
        self.assertEqual(result, expected_postfix)

    def test_expression_with_parentheses(self):
        """
        Prueba la correcta evaluación de expresiones con paréntesis.
        """
        expr = "(a|b)*.c"
        expected_postfix = ["a", "b", "|", "*", "c", "."]
        result = [s.name for s in shunting_yard(expr)]
        self.assertEqual(result, expected_postfix)

    def test_expression_with_optional_and_positive_closure(self):
        """
        Prueba operadores como ? y + en la conversión.
        """
        expr = "a?.b+"
        expected_postfix = ["a", "?", "b", "+", "."]
        result = [s.name for s in shunting_yard(expr)]
        self.assertEqual(result, expected_postfix)

if __name__ == "__main__":
    unittest.main()
