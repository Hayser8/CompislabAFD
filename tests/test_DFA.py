import unittest
from parser import parse_regex, to_postfix
from preprocessor import preprocess_expression
from symbol import Symbol
from arbolSINT import SyntaxTree
from DFA import DFA

def simulate_dfa(dfa, input_string):
    """
    Función auxiliar para simular la ejecución del DFA.
    Recorre la cadena de entrada y retorna True si termina en un estado final.
    """
    current_state = dfa.start_state
    for ch in input_string:
        if current_state in dfa.transitions and ch in dfa.transitions[current_state]:
            current_state = dfa.transitions[current_state][ch]
        else:
            return False
    return current_state in dfa.final_states

class TestDFA(unittest.TestCase):
    def build_dfa(self, regex):
        preprocessed = preprocess_expression(regex)
        ast = parse_regex(preprocessed)
        postfix = to_postfix(ast)
        # Tokenizamos la cadena postfix (muy similar a la función tokenize_postfix)
        tokens = []
        for token in postfix.split():
            if token.startswith("lit(") and token.endswith(")"):
                literal = token[4:-1]
                tokens.append(Symbol(literal, "operand"))
            elif token in {'*', '|', '·', '?', '+'}:
                tokens.append(Symbol(token, "operator"))
            else:
                tokens.append(Symbol(token, "operand"))
        st = SyntaxTree(tokens)
        return DFA(st)

    def test_dfa_accepts_a(self):
        dfa = self.build_dfa("a")
        self.assertTrue(simulate_dfa(dfa, "a"))
        self.assertFalse(simulate_dfa(dfa, "b"))

    def test_dfa_accepts_ab(self):
        dfa = self.build_dfa("ab")
        self.assertTrue(simulate_dfa(dfa, "ab"))
        self.assertFalse(simulate_dfa(dfa, "a"))
        self.assertFalse(simulate_dfa(dfa, "b"))

if __name__ == '__main__':
    unittest.main()
