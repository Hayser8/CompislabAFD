import unittest
from symbol import Symbol
from parser import (
    Parser, parse_regex, Literal, Concat, Alternation, Star, Plus, Group, Epsilon, to_postfix
)

class TestParser(unittest.TestCase):

    def test_literal(self):
        ast = parse_regex("a")
        self.assertIsInstance(ast, Literal)
        self.assertEqual(ast.value, "a")

    def test_concat(self):
        ast = parse_regex("ab")
        self.assertIsInstance(ast, Concat)
        self.assertIsInstance(ast.left, Literal)
        self.assertIsInstance(ast.right, Literal)
        self.assertEqual(ast.left.value, "a")
        self.assertEqual(ast.right.value, "b")

    def test_alternation(self):
        ast = parse_regex("a|b")
        self.assertIsInstance(ast, Alternation)
        self.assertIsInstance(ast.left, Literal)
        self.assertIsInstance(ast.right, Literal)
        self.assertEqual(ast.left.value, "a")
        self.assertEqual(ast.right.value, "b")

    def test_star(self):
        ast = parse_regex("a*")
        self.assertIsInstance(ast, Star)
        self.assertIsInstance(ast.child, Literal)
        self.assertEqual(ast.child.value, "a")

    def test_plus(self):
        ast = parse_regex("a+")
        self.assertIsInstance(ast, Plus)
        self.assertIsInstance(ast.child, Literal)
        self.assertEqual(ast.child.value, "a")

    def test_group(self):
        ast = parse_regex("(ab)")
        self.assertIsInstance(ast, Group)
        self.assertIsInstance(ast.child, Concat)
        self.assertEqual(ast.child.left.value, "a")
        self.assertEqual(ast.child.right.value, "b")

    def test_nested_group(self):
        ast = parse_regex("((a|b)*)")
        self.assertIsInstance(ast, Group)
        self.assertIsInstance(ast.child, Star)
        self.assertIsInstance(ast.child.child, Group)
        self.assertIsInstance(ast.child.child.child, Alternation)
        self.assertEqual(ast.child.child.child.left.value, "a")
        self.assertEqual(ast.child.child.child.right.value, "b")

    def test_empty_expression(self):
        ast = parse_regex("")
        self.assertIsInstance(ast, Epsilon)

    def test_invalid_expression_unmatched_paren(self):
        with self.assertRaises(ValueError):
            parse_regex("(ab")

    def test_invalid_expression_unmatched_brace(self):
        with self.assertRaises(ValueError):
            parse_regex("{ab")

    def test_postfix_conversion(self):
        ast = parse_regex("a|b")
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a b |")

        ast = parse_regex("ab")
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a b .")

        ast = parse_regex("a*")
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a *")

        ast = parse_regex("(a|b)*")
        postfix = to_postfix(ast)
        self.assertEqual(postfix, "a b | *")

if __name__ == '__main__':
    unittest.main()
