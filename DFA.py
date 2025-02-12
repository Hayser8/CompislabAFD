from graphviz import Digraph
import re

class DFA:
    """
    Construcción del DFA a partir del árbol sintáctico.
    """
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree
        # El estado inicial es el conjunto firstpos de la raíz.
        self.start_state = frozenset(syntax_tree.root.firstpos)
        self.transitions = {}
        self.final_states = set()
        self.build_dfa()

    def build_dfa(self):
        unmarked_states = [self.start_state]
        dfa_states = {self.start_state: 0}
        state_counter = 1

        while unmarked_states:
            current = unmarked_states.pop()
            self.transitions[dfa_states[current]] = {}
            # Se extraen los símbolos (operandos) presentes en el estado actual, excluyendo 'ε' y '#'.
            symbols = {node.symbol.name for node in current 
                       if node.symbol.type == "operand" and node.symbol.name not in {'ε', '#'}}
            # Para cada símbolo, se calcula la unión de followpos de cada nodo de current que tenga ese símbolo.
            for symbol in symbols:
                next_set = set()
                for node in current:
                    if node.symbol.name == symbol:
                        next_set.update(self.syntax_tree.followpos.get(node, set()))
                next_state = frozenset(next_set)
                if next_state:
                    if next_state not in dfa_states:
                        dfa_states[next_state] = state_counter
                        state_counter += 1
                        unmarked_states.append(next_state)
                    self.transitions[dfa_states[current]][symbol] = dfa_states[next_state]
            # Si el conjunto actual contiene el nodo con el end marker '#' se marca como final.
            for node in current:
                if node.symbol.name == '#':
                    self.final_states.add(dfa_states[current])
                    break

    def visualize(self, filename="dfa"):
        filename = re.sub(r'[^a-zA-Z0-9_]', '_', filename)
        dot = Digraph()
        for state, transitions in self.transitions.items():
            shape = "doublecircle" if state in self.final_states else "circle"
            dot.node(str(state), str(state), shape=shape)
            for symbol, target in transitions.items():
                dot.edge(str(state), str(target), label=symbol)
        dot.render(filename, format="png", cleanup=True)
