import unittest
from preprocessor import preprocess_expression_manual

class TestCommentPatterns(unittest.TestCase):

    def test_multiline_comment_complete(self):
        # Prueba de comentario de bloque completo
        pattern = "('/*' ([^*] | '*' [^/])* '*' '/')"
        preprocessed = preprocess_expression_manual(pattern)
        # Se espera que el literal procesado empiece con "LIT<<" y termine con ">>"
        self.assertTrue(preprocessed.startswith("LIT<<"), "El preprocesado debe producir un literal")
        self.assertTrue(preprocessed.endswith(">>"), "El preprocesado debe producir un literal")
        # Además debe contener las secuencias de apertura y cierre de comentario de bloque
        self.assertIn("/*", preprocessed, "Debe contener la secuencia de apertura '/*'")
        self.assertIn("*/", preprocessed, "Debe contener la secuencia de cierre '*/'")

    def test_multiline_comment_incomplete(self):
        # Prueba de comentario de bloque incompleto (falta el cierre final)
        pattern_incomplete = "('/*' ([^*] | '*' [^/])* '*' "
        with self.assertRaises(ValueError):
            preprocess_expression_manual(pattern_incomplete)

    def test_single_line_comment_complete(self):
        # Prueba de comentario de línea completo
        pattern = "'//' [^\\n]* '\\n'"
        preprocessed = preprocess_expression_manual(pattern)
        self.assertTrue(preprocessed.startswith("LIT<<"), "El preprocesado debe producir un literal")
        self.assertTrue(preprocessed.endswith(">>"), "El preprocesado debe producir un literal")
        # Verificamos que contenga la secuencia de inicio de comentario y el salto de línea final
        self.assertIn("//", preprocessed, "Debe contener la secuencia de apertura '//'")
        self.assertIn("\n", preprocessed, "Debe contener el carácter de nueva línea '\\n'")

    def test_single_line_comment_incomplete(self):
        # Prueba de comentario de línea incompleto (falta la comilla de cierre en el literal final)
        pattern_incomplete = "'//' [^\\n]* '\\n"  # Literal sin cerrar
        with self.assertRaises(ValueError):
            preprocess_expression_manual(pattern_incomplete)

if __name__ == "__main__":
    unittest.main()
