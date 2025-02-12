from graphviz import Digraph
import re

class DFA:
    """
    Construcción del AFD a partir del árbol sintáctico.
    """
    def __init__(self, syntax_tree):
        self.syntax_tree = syntax_tree
        self.start_state = frozenset(syntax_tree.root.firstpos)
        self.transitions = {}
        self.final_states = set()
        self.build_dfa()

    def build_dfa(self):
        """Construye el AFD a partir de firstpos y followpos."""
        unmarked_states = [self.start_state]
        dfa_states = {self.start_state: 0}  # Estado inicial etiquetado como 0
        state_counter = 1
        symbols = set(node.symbol.name for node in self.start_state if node.symbol.type == "operand")
        
        while unmarked_states:
            current_state = unmarked_states.pop()
            self.transitions[dfa_states[current_state]] = {}
            print(f"Procesando estado {dfa_states[current_state]}: {sorted(node.symbol.name for node in current_state)}")
            
            for symbol in symbols:
                next_state = frozenset(
                    follow for node in current_state if node.symbol.name == symbol for follow in self.syntax_tree.followpos.get(node, [])
                )
                
                if next_state:
                    if next_state not in dfa_states:
                        dfa_states[next_state] = state_counter
                        state_counter += 1
                        unmarked_states.append(next_state)
                    self.transitions[dfa_states[current_state]][symbol] = dfa_states[next_state]
                    print(f"  Transición con '{symbol}' -> Estado {dfa_states[next_state]}")
                    
            if any(node.symbol.name == '#' for node in current_state):  # '#' representa el estado de aceptación
                self.final_states.add(dfa_states[current_state])
                print(f"  Estado {dfa_states[current_state]} es final")
    
    def visualize(self, filename="dfa"):
        """Genera la visualización del AFD con Graphviz."""
        filename = re.sub(r'[^a-zA-Z0-9_]', '_', filename)
        dot = Digraph()
        
        for state, transitions in self.transitions.items():
            shape = "doublecircle" if state in self.final_states else "circle"
            dot.node(str(state), str(state), shape=shape)
            
            for symbol, target in transitions.items():
                dot.edge(str(state), str(target), label=symbol)
        
        dot.render(filename, format="png", cleanup=True)

    def visualize(self, filename="dfa"):
        """Genera la visualización del AFD con Graphviz."""
        filename = re.sub(r'[^a-zA-Z0-9_]', '_', filename)
        dot = Digraph()
        
        for state, transitions in self.transitions.items():
            shape = "doublecircle" if state in self.final_states else "circle"
            dot.node(str(state), str(state), shape=shape)
            
            for symbol, target in transitions.items():
                dot.edge(str(state), str(target), label=symbol)
        
        dot.render(filename, format="png", cleanup=True)

