import unittest
from preprocessor import preprocess_expression

class TestPreprocessor(unittest.TestCase):

    def test_expand_range(self):
        self.assertEqual(preprocess_expression("[a-c]"), "(a|b|c)")
        self.assertEqual(preprocess_expression("[0-3]"), "(0|1|2|3)")

    def test_expand_list(self):
        self.assertEqual(preprocess_expression("[abc]"), "(a|b|c)")
        self.assertEqual(preprocess_expression("[135]"), "(1|3|5)")

    def test_replace_escaped(self):
        self.assertEqual(preprocess_expression(r"\+"), "§+")
        self.assertEqual(preprocess_expression(r"\?"), "§?")
        self.assertEqual(preprocess_expression(r"\t"), "§t")
        self.assertEqual(preprocess_expression(r"\n"), "§n")
        self.assertEqual(preprocess_expression(r"\("), "(")
        self.assertEqual(preprocess_expression(r"\)"), ")")

    def test_remove_spaces(self):
        self.assertEqual(preprocess_expression(" a b c "), "abc")
        self.assertEqual(preprocess_expression("x | y "), "x|y")

    def test_quantifier_transformation(self):
        self.assertEqual(preprocess_expression("a+"), "(a.a*)")
        self.assertEqual(preprocess_expression("b?"), "(b|ε)")
        self.assertEqual(preprocess_expression("(ab)+"), "((ab).(ab)*)")
        self.assertEqual(preprocess_expression("{xyz}+"), "({xyz}.{xyz}*)")

    def test_nested_groups_with_quantifiers(self):
        self.assertEqual(preprocess_expression("{a+}"), "({a}.{a}*)")
        self.assertEqual(preprocess_expression("{b?}"), "({b}|ε)")

    def test_combined_cases(self):
        self.assertEqual(preprocess_expression("a|b+"), "a|(b.b*)")
        self.assertEqual(preprocess_expression("x?y*"), "(x|ε)y*")
        self.assertEqual(preprocess_expression("[0-2]+"), "((0|1|2).(0|1|2)*)")

    def test_escape_special_characters(self):
        self.assertEqual(preprocess_expression(r"\+"), "§+")
        self.assertEqual(preprocess_expression(r"\?"), "§?")
        self.assertEqual(preprocess_expression(r"\*"), "§*")
        self.assertEqual(preprocess_expression(r"\|"), "§|")
        self.assertEqual(preprocess_expression(r"\."), "§.")
        self.assertEqual(preprocess_expression(r"\^"), "§^")
        self.assertEqual(preprocess_expression(r"\$"), "§$")

if __name__ == '__main__':
    unittest.main()
