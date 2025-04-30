import unittest
from parser.grammar import Grammar, Terminal, NonTerminal, Production
from parser.lr0 import Item, closure, goto, build_canonical

class TestLR0(unittest.TestCase):

    def setUp(self):
        self.t_PLUS = Terminal("PLUS")
        self.t_NUM = Terminal("NUM")
        self.nt_Expr = NonTerminal("Expr")

        # Expr → Expr PLUS NUM | NUM
        self.p1 = Production(id=0, head="Expr", body=(self.nt_Expr, self.t_PLUS, self.t_NUM))
        self.p2 = Production(id=1, head="Expr", body=(self.t_NUM,))

        self.grammar = Grammar(
            terminals={self.t_PLUS, self.t_NUM},
            non_terminals={self.nt_Expr},
            productions=[self.p1, self.p2],
            start_symbol=self.nt_Expr
        )

    def test_item_repr_and_advance(self):
        item = Item(self.p1, 1)
        self.assertEqual(str(item), "Expr → Expr · PLUS NUM")
        next_item = item.advance_dot()
        self.assertEqual(next_item.dot, 2)

    def test_closure_includes_initial_items(self):
        initial = Item(self.p2, 0)
        closure_set = closure(self.grammar, {initial})
        self.assertIn(initial, closure_set)
        self.assertEqual(len(closure_set), 1)

    def test_goto_advances_and_closes(self):
        item = Item(self.p1, 0)  # Expr → · Expr PLUS NUM
        closure_set = closure(self.grammar, {item})
        result = goto(self.grammar, closure_set, self.nt_Expr)
        self.assertTrue(any(i.dot == 1 for i in result))  # Should contain Expr → Expr · PLUS NUM

    def test_build_canonical_states(self):
        states = build_canonical(self.grammar)
        self.assertTrue(len(states) >= 2)
        self.assertTrue(any(state for state in states if any(item.dot == 1 for item in state.items)))

if __name__ == "__main__":
    unittest.main()
