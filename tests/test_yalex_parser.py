import unittest
from lexer.yalex_parser import YALexParser

class TestYALexParser(unittest.TestCase):
    def setUp(self):
        with open("test.yal", "w", encoding="utf-8") as f:
            f.write("""
{
import tokens
}

let digit = ['0'-'9']
let letter = ['a'-'z' 'A'-'Z']

rule gettoken =
['0'-'9']+ { return "NUMBER" }
| ['a'-'z' 'A'-'Z']+ { return "IDENTIFIER" }
| '+' { return "PLUS" }
| '-' { return "MINUS" }
| eof { return "EOF" }

{
print("Fin del archivo")
}
""")

    def test_parser(self):
        parser = YALexParser("test.yal")
        
        self.assertEqual(parser.get_header().strip(), "import tokens")
        self.assertEqual(parser.get_trailer().strip(), 'print("Fin del archivo")')

        tokens = parser.get_tokens()
        self.assertEqual(tokens["digit"], "['0'-'9']")
        self.assertEqual(tokens["letter"], "['a'-'z' 'A'-'Z']")

        rules = parser.get_rules()
        self.assertIn("gettoken", rules)
        self.assertEqual(rules["gettoken"][0], ("['0'-'9']+", 'return "NUMBER"'))
        self.assertEqual(rules["gettoken"][1], ("['a'-'z' 'A'-'Z']+", 'return "IDENTIFIER"'))
        self.assertEqual(rules["gettoken"][2], ("'+'", 'return "PLUS"'))
        self.assertEqual(rules["gettoken"][3], ("'-'", 'return "MINUS"'))
        self.assertEqual(rules["gettoken"][4], ("eof", 'return "EOF"'))

if __name__ == "__main__":
    unittest.main()
