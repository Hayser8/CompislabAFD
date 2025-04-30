import unittest
from parser.grammar import Terminal, NonTerminal, Production, Grammar
from parser.first_follow import FirstFollowCalculator

class TestFirstFollowCalculator(unittest.TestCase):

    def setUp(self):
        print("\n[Setup] Construyendo gramática para FIRST/FOLLOW...")

        # Símbolos
        self.t_NUM = Terminal("NUM")
        self.t_PLUS = Terminal("PLUS")
        self.nt_Expr = NonTerminal("Expr")

        # Producciones
        self.p1 = Production(id=0, head="Expr", body=(self.nt_Expr, self.t_PLUS, self.t_NUM))
        self.p2 = Production(id=1, head="Expr", body=(self.t_NUM,))

        # Gramática
        self.grammar = Grammar(
            terminals={self.t_NUM, self.t_PLUS},
            non_terminals={self.nt_Expr},
            productions=[self.p1, self.p2],
            start_symbol=self.nt_Expr
        )

        self.calculator = FirstFollowCalculator(self.grammar)

    def test_first_sets(self):
        print("\n[Test] FIRST sets")
        first_expr = self.calculator.get_first(self.nt_Expr)
        print(f"FIRST(Expr): {first_expr}")
        self.assertIn(self.t_NUM, first_expr)

    def test_follow_sets(self):
        print("\n[Test] FOLLOW sets")
        follow_expr = self.calculator.get_follow(self.nt_Expr)
        print(f"FOLLOW(Expr): {follow_expr}")
        self.assertIn(Terminal('$'), follow_expr)
        self.assertIn(self.t_PLUS, follow_expr)

    def test_no_epsilon_in_terminals(self):
        print("\n[Test] No ε en terminales")
        for term in self.grammar.terminals:
            first_set = self.calculator.get_first(term)
            self.assertNotIn(Terminal("ε"), first_set)
            print(f"FIRST({term}): {first_set}")

if __name__ == '__main__':
    unittest.main()
