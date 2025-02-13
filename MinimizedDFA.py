from DFA import DFA
from graphviz import Digraph

def escape_label(label):
    """
    Escapa caracteres especiales en la etiqueta para Graphviz.
    Se escapan la barra invertida, las comillas dobles y las llaves.
    """
    return (
        label.replace("\\", "\\\\")
             .replace('"', '\\"')
             .replace("{", "\\{")
             .replace("}", "\\}")
    )

class MinimizedDFA:
    def __init__(self, dfa: DFA):
        """
        Recibe un objeto DFA (con transiciones, estados finales, etc.)
        y construye la versión minimizada mediante el algoritmo de partición.
        """
        self.original_dfa = dfa
        self.start_state = dfa.start_state
        self.transitions = dfa.transitions
        self.final_states = dfa.final_states
        self.states = set(self.transitions.keys())
        for s in dfa.final_states:
            self.states.add(s)
        self.states = self._get_reachable_states()
        P = [set(), set()]
        for state in self.states:
            if state in self.final_states:
                P[0].add(state)
            else:
                P[1].add(state)
        P = [part for part in P if part]  
        W = [part.copy() for part in P]
        alphabet = set()
        for state in self.states:
            if state in self.transitions:
                for sym in self.transitions[state]:
                    alphabet.add(sym)
        while W:
            A = W.pop()
            for c in alphabet:
                X = set()
                for state in self.states:
                    if state in self.transitions and c in self.transitions[state]:
                        if self.transitions[state][c] in A:
                            X.add(state)
                new_P = []
                for Y in P:
                    intersection = Y.intersection(X)
                    difference = Y.difference(X)
                    if intersection and difference:
                        new_P.append(intersection)
                        new_P.append(difference)
                        if Y in W:
                            W.remove(Y)
                            W.append(intersection)
                            W.append(difference)
                        else:
                            if len(intersection) <= len(difference):
                                W.append(intersection)
                            else:
                                W.append(difference)
                    else:
                        new_P.append(Y)
                P = new_P
        self.P = P  
        self.minimized_transitions = {}
        self.minimized_states = set()
        self.minimized_final = set()
        for block in P:
            block_fro = frozenset(block)
            self.minimized_states.add(block_fro)
            if any(state in self.final_states for state in block):
                self.minimized_final.add(block_fro)
        for block in P:
            if self.start_state in block:
                self.minimized_start = frozenset(block)
                break
        for block in P:
            block_fro = frozenset(block)
            self.minimized_transitions[block_fro] = {}
            representative = next(iter(block))
            if representative in self.transitions:
                for c, target in self.transitions[representative].items():
                    for block2 in P:
                        if target in block2:
                            self.minimized_transitions[block_fro][c] = frozenset(block2)
                            break
        self.eof_symbol = dfa.eof_symbol

    def _get_reachable_states(self):
        """
        Obtiene el conjunto de estados alcanzables desde el estado inicial.
        """
        reachable = set()
        worklist = [self.start_state]
        reachable.add(self.start_state)
        while worklist:
            state = worklist.pop(0)
            if state in self.transitions:
                for sym, target in self.transitions[state].items():
                    if target not in reachable:
                        reachable.add(target)
                        worklist.append(target)
        return reachable

    def visualize(self, filename='min_dfa'):
        """
        Genera y guarda la visualización del DFA minimizado usando Graphviz.
        """
        dot = Digraph(comment='Minimized DFA')
        state_ids = {}
        counter = 0
        for state in self.minimized_states:
            state_ids[state] = f"M{counter}"
            counter += 1
        for state, sid in state_ids.items():
            label = "{" + ", ".join(str(s) for s in sorted(state)) + "}"
            shape = "doublecircle" if state in self.minimized_final else "circle"
            dot.node(sid, label=escape_label(label), shape=shape)
        if self.minimized_start in state_ids:
            dot.node("start", shape="none", label="")
            dot.edge("start", state_ids[self.minimized_start])
        for state, trans in self.minimized_transitions.items():
            for c, target in trans.items():
                dot.edge(state_ids[state], state_ids[target], label=escape_label(c))
        dot.render(filename, format="png", cleanup=True)
        print(f"Minimized DFA image generated: {filename}.png")
