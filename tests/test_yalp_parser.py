import unittest
from parser.yalp_lexer import tokenize
from parser.yalp_parser import YalpParser
from parser.grammar import Terminal, NonTerminal, Production

class TestYalpParser(unittest.TestCase):

    def setUp(self):
        self.sample_input = """
        /* Definición de parser */
        %token NUM PLUS
        IGNORE WS
        %%
        Expr :
            Expr PLUS NUM
          | NUM
        ;
        """

        self.tokens = list(tokenize(self.sample_input))
        self.parser = YalpParser(self.tokens)
        self.grammar = self.parser.parse()

    def test_terminals_and_nonterminals(self):
        self.assertIn(Terminal("NUM"), self.grammar.terminals)
        self.assertIn(NonTerminal("Expr"), self.grammar.non_terminals)

    def test_start_symbol(self):
        self.assertEqual(str(self.grammar.start_symbol), "Expr")

    def test_production_count(self):
        self.assertEqual(len(self.grammar.productions), 2)

    def test_production_structure(self):
        prod0 = self.grammar.productions[0]
        self.assertEqual(prod0.head, "Expr")
        self.assertEqual([str(s) for s in prod0.body], ["Expr", "PLUS", "NUM"])

if __name__ == "__main__":
    unittest.main()
