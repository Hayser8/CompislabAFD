import unittest
from parser import parse_regex, to_postfix

class TestParser(unittest.TestCase):
    def test_alternation(self):
        expr = "a|b"
        ast = parse_regex(expr)
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a b |")

    def test_concatenation(self):
        expr = "ab"
        ast = parse_regex(expr)
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a b ·")

    def test_star(self):
        expr = "a*"
        ast = parse_regex(expr)
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a *")

    def test_plus(self):
        expr = "a+"
        ast = parse_regex(expr)
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a a * ·")

if __name__ == '__main__':
    unittest.main()
