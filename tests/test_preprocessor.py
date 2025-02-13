import unittest
from preprocessor import preprocess_expression

class TestPreprocessor(unittest.TestCase):
    def test_no_change(self):
        # Sin espacios ni caracteres especiales, la expresión se mantiene igual.
        expr = "abc"
        result = preprocess_expression(expr)
        self.assertEqual(result, "abc")

    def test_escape(self):
        # Verifica que se antepone el marcador de escape ( § )
        expr = r"\+"
        result = preprocess_expression(expr)
        self.assertIn("§+", result)

    def test_range_expansion(self):
        # Se espera que [0-3] se expanda a (0|1|2|3)
        expr = "[0-3]"
        result = preprocess_expression(expr)
        self.assertEqual(result, "(0|1|2|3)")

    def test_list_expansion(self):
        # Se espera que [ae03] se expanda a (a|e|0|3)
        expr = "[ae03]"
        result = preprocess_expression(expr)
        self.assertEqual(result, "(a|e|0|3)")

if __name__ == '__main__':
    unittest.main()
