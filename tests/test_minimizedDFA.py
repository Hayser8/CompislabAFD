import unittest
from parser import parse_regex, to_postfix
from preprocessor import preprocess_expression
from symbol import Symbol
from arbolSINT import SyntaxTree
from DFA import DFA
from MinimizedDFA import MinimizedDFA

def simulate_dfa(dfa, input_string, minimized=False):
    """
    Función auxiliar para simular la ejecución del DFA (original o minimizado).
    """
    if minimized:
        transitions = dfa.minimized_transitions
        current_state = dfa.minimized_start
        final_states = dfa.minimized_final
    else:
        transitions = dfa.transitions
        current_state = dfa.start_state
        final_states = dfa.final_states
    for ch in input_string:
        if current_state in transitions and ch in transitions[current_state]:
            current_state = transitions[current_state][ch]
        else:
            return False
    return current_state in final_states

class TestMinimizedDFA(unittest.TestCase):
    def build_min_dfa(self, regex):
        preprocessed = preprocess_expression(regex)
        ast = parse_regex(preprocessed)
        postfix = to_postfix(ast)
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
        dfa = DFA(st)
        return MinimizedDFA(dfa)

    def test_minimized_dfa_accepts_a(self):
        min_dfa = self.build_min_dfa("a")
        self.assertTrue(simulate_dfa(min_dfa, "a", minimized=True))
        self.assertFalse(simulate_dfa(min_dfa, "b", minimized=True))

    def test_minimized_dfa_accepts_ab(self):
        min_dfa = self.build_min_dfa("ab")
        self.assertTrue(simulate_dfa(min_dfa, "ab", minimized=True))
        self.assertFalse(simulate_dfa(min_dfa, "a", minimized=True))
        self.assertFalse(simulate_dfa(min_dfa, "b", minimized=True))

if __name__ == '__main__':
    unittest.main()
