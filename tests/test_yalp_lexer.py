import unittest
from parser.yalp_lexer import tokenize, Tok

class TestYalpLexer(unittest.TestCase):

    def test_tokenize_simple(self):
        yalp_input = """
        %token NUM PLUS
        IGNORE WS
        %%
        Expr : Expr PLUS NUM | NUM ;
        """
        tokens = list(tokenize(yalp_input))

        types = [t.type for t in tokens]
        lexemes = [t.lexeme for t in tokens]

        expected_types = [
            "PERCENT_TOKEN", "IDENTIFIER", "IDENTIFIER",  # %token NUM PLUS
            "IGNORE", "IDENTIFIER",                       # IGNORE WS
            "PERCENT_PERCENT",                            # %%
            "IDENTIFIER", ":", "IDENTIFIER", "IDENTIFIER", "IDENTIFIER",
            "|", "IDENTIFIER", ";"
        ]

        expected_lexemes = [
            "%token", "NUM", "PLUS",
            "IGNORE", "WS",
            "%%",
            "Expr", ":", "Expr", "PLUS", "NUM",
            "|", "NUM", ";"
        ]

        self.assertEqual(types, expected_types)
        self.assertEqual(lexemes, expected_lexemes)

    def test_tokenize_with_comments(self):
        yalp_input = """
        /* Comentario al inicio */
        %token ID /* comentario inline */ PLUS
        %%
        Rule : ID | PLUS ;
        """
        tokens = list(tokenize(yalp_input))

        # Confirmamos que los comentarios no afectaron los tokens
        self.assertTrue(any(t.lexeme == "ID" for t in tokens))
        self.assertTrue(any(t.lexeme == "PLUS" for t in tokens))
        self.assertTrue(any(t.lexeme == "Rule" for t in tokens))
        self.assertTrue(all("/*" not in t.lexeme for t in tokens))  # Nada debería tener comentario

    def test_tokenize_unexpected_character(self):
        yalp_input = "%token X\n@"
        with self.assertRaises(SyntaxError):
            list(tokenize(yalp_input))

if __name__ == "__main__":
    unittest.main()
