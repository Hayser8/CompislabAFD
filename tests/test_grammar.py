import unittest
from parser.grammar import Terminal, NonTerminal, Production, Grammar

class TestGrammarModule(unittest.TestCase):

    def setUp(self):
        print("\n[Setup] Inicializando símbolos, producciones y gramática...")

        self.t_NUM = Terminal("NUM")
        self.t_PLUS = Terminal("PLUS")
        self.nt_Expr = NonTerminal("Expr")
        
        self.p1 = Production(id=0, head="Expr", body=(self.nt_Expr, self.t_PLUS, self.t_NUM))
        self.p2 = Production(id=1, head="Expr", body=(self.t_NUM,))

        self.grammar = Grammar(
            terminals={self.t_NUM, self.t_PLUS},
            non_terminals={self.nt_Expr},
            productions=[self.p1, self.p2],
            start_symbol=self.nt_Expr
        )

        print(f"[Setup] Producciones: {self.p1}, {self.p2}")
        print(f"[Setup] Terminales: {self.grammar.terminals}")
        print(f"[Setup] No terminales: {self.grammar.non_terminals}")
        print(f"[Setup] Símbolo inicial: {self.grammar.start_symbol}")

    def test_terminal_and_nonterminal_repr(self):
        print("\n[Test] test_terminal_and_nonterminal_repr")
        print(f"  Repr Terminal: {repr(self.t_NUM)}")
        print(f"  Repr No-Terminal: {repr(self.nt_Expr)}")
        self.assertEqual(repr(self.t_NUM), "NUM")
        self.assertEqual(repr(self.nt_Expr), "Expr")

    def test_production_repr(self):
        print("\n[Test] test_production_repr")
        print(f"  Producción p1: {repr(self.p1)}")
        expected = "Expr → Expr PLUS NUM"
        self.assertEqual(repr(self.p1), expected)

    def test_grammar_construction(self):
        print("\n[Test] test_grammar_construction")
        print(f"  Terminales en gramática: {self.grammar.terminals}")
        print(f"  No terminales en gramática: {self.grammar.non_terminals}")
        self.assertIn(self.t_PLUS, self.grammar.terminals)
        self.assertIn(self.nt_Expr, self.grammar.non_terminals)
        self.assertEqual(len(self.grammar.productions), 2)
        self.assertEqual(self.grammar.start_symbol, self.nt_Expr)

    def test_augmented_grammar(self):
        print("\n[Test] test_augmented_grammar")
        augmented = self.grammar.augmented()
        print(f"  Símbolo inicial original: {self.grammar.start_symbol}")
        print(f"  Nuevo símbolo inicial: {augmented.start_symbol}")
        print(f"  Nueva producción: {augmented.productions[0]}")
        self.assertIn(NonTerminal("Expr'"), augmented.non_terminals)
        self.assertEqual(augmented.start_symbol.name, "Expr'")
        self.assertEqual(augmented.productions[0].head, "Expr'")
        self.assertEqual(augmented.productions[0].body, (self.nt_Expr,))

if __name__ == '__main__':
    unittest.main()
