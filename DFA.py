from graphviz import Digraph

def escape_label(label):
    """
    Escapa caracteres especiales en la etiqueta para Graphviz.
    Ahora se escapan:
      - La barra invertida (\) → \\
      - Las comillas dobles (") → \"
      - Las llaves ({ y }) → \{ y \}
    """
    return (
        label
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("{", "\\{")
        .replace("}", "\\}")
    )

class DFA:
    def __init__(self, syntax_tree):
        """
        Recibe un objeto SyntaxTree (definido en arbolSINT.py) y construye
        el DFA mediante el método directo (usando nullable, firstpos, lastpos y followpos).
        """
        self.followpos = {}       
        self.pos_to_symbol = {}   
        pos_counter = [1]         
        self.nullable, self.firstpos, self.lastpos = self.compute_functions(
            syntax_tree.root, self.followpos, self.pos_to_symbol, pos_counter
        )
        self.start_state = frozenset(self.firstpos)
        self.eof_symbol = '☒'
        self.eof_position = None
        for pos, symbol in self.pos_to_symbol.items():
            if symbol == self.eof_symbol:
                self.eof_position = pos
                break
        self.build_dfa()

    def compute_functions(self, node, followpos, pos_to_symbol, pos_counter):
        """
        Función recursiva que computa para cada nodo del árbol:
          - nullable: True si la subexpresión puede ser ε.
          - firstpos: conjunto de posiciones (números de hoja) que pueden aparecer al inicio.
          - lastpos: conjunto de posiciones que pueden aparecer al final.
        
        Además, asigna números de posición a cada hoja (excepto ε) y actualiza followpos.
        """
        if node.left is None and node.right is None:
            if node.value == "ε":
                return (True, set(), set())
            else:
                pos = pos_counter[0]
                pos_counter[0] += 1
                node.pos = pos  
                pos_to_symbol[pos] = node.value
                return (False, {pos}, {pos})
        elif node.value == '|':
            left_nullable, left_firstpos, left_lastpos = self.compute_functions(node.left, followpos, pos_to_symbol, pos_counter)
            right_nullable, right_firstpos, right_lastpos = self.compute_functions(node.right, followpos, pos_to_symbol, pos_counter)
            nullable = left_nullable or right_nullable
            firstpos = left_firstpos.union(right_firstpos)
            lastpos = left_lastpos.union(right_lastpos)
            return (nullable, firstpos, lastpos)
        elif node.value == '·':
            left_nullable, left_firstpos, left_lastpos = self.compute_functions(node.left, followpos, pos_to_symbol, pos_counter)
            right_nullable, right_firstpos, right_lastpos = self.compute_functions(node.right, followpos, pos_to_symbol, pos_counter)
            nullable = left_nullable and right_nullable
            firstpos = left_firstpos.union(right_firstpos) if left_nullable else left_firstpos
            lastpos = left_lastpos.union(right_lastpos) if right_nullable else right_lastpos
            for pos in left_lastpos:
                followpos.setdefault(pos, set()).update(right_firstpos)
            return (nullable, firstpos, lastpos)
        elif node.value == '*':
            child_nullable, child_firstpos, child_lastpos = self.compute_functions(node.left, followpos, pos_to_symbol, pos_counter)
            nullable = True
            firstpos = child_firstpos
            lastpos = child_lastpos
            for pos in child_lastpos:
                followpos.setdefault(pos, set()).update(child_firstpos)
            return (nullable, firstpos, lastpos)
        else:
            raise Exception("Operador no soportado en la construcción del DFA: " + node.value)

    def build_dfa(self):
        """
        Construye el DFA a partir de la información followpos.
        Cada estado es un conjunto (frozenset) de posiciones.
        Se generan las transiciones y se determinan los estados finales.
        """
        self.transitions = {}   
        self.final_states = set()
        unmarked_states = []
        dfa_states = {}

        start = self.start_state
        unmarked_states.append(start)
        dfa_states[start] = True

        while unmarked_states:
            state = unmarked_states.pop(0)
            self.transitions[state] = {}
            symbols = {}
            for pos in state:
                sym = self.pos_to_symbol[pos]
                if sym == self.eof_symbol or sym == "ε":
                    continue
                symbols.setdefault(sym, set()).update(self.followpos.get(pos, set()))
            for sym, pos_set in symbols.items():
                next_state = frozenset(pos_set)
                if not next_state:
                    continue
                self.transitions[state][sym] = next_state
                if next_state not in dfa_states:
                    dfa_states[next_state] = True
                    unmarked_states.append(next_state)
        for state in dfa_states:
            if self.eof_position is not None and self.eof_position in state:
                self.final_states.add(state)

    def visualize(self, filename='dfa'):
        """
        Genera y guarda la visualización del DFA usando Graphviz.
        """
        dot = Digraph(comment='DFA')
        state_ids = {}
        counter = 0
        for state in self.transitions:
            state_ids[state] = f"S{counter}"
            counter += 1
        for state in self.final_states:
            if state not in state_ids:
                state_ids[state] = f"S{counter}"
                counter += 1
        for state, sid in state_ids.items():
            label = str(set(state))
            dot.node(sid, label=escape_label(label),
                     shape="doublecircle" if state in self.final_states else "circle")
        if self.start_state in state_ids:
            dot.node("start", shape="none", label="")
            dot.edge("start", state_ids[self.start_state])
        for state, trans in self.transitions.items():
            for sym, next_state in trans.items():
                dot.edge(state_ids[state], state_ids[next_state], label=escape_label(sym))
        dot.render(filename, format="png", cleanup=True)
        print(f"DFA image generated: {filename}.png")
