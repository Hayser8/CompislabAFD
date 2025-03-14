from graphviz import Digraph

class MinimizedDFA:
    def __init__(self, dfa):
        self.original_dfa = dfa
        # Copiamos lo que necesitemos
        self.states = list(dfa.states)          # array de frozensets
        self.transitions = dict(dfa.transitions)
        self.final_states = set(dfa.final_states)
        self.alphabet = set(dfa.alphabet)
        
        # Mapeamos cada conjunto (state) con un índice
        self.state_to_index = {st: i for i, st in enumerate(self.states)}
        
        # Aplicar el algoritmo de minimización
        self._minimize()
    
    def _minimize(self):
        # Partición inicial: finales vs no finales
        P = []
        finals = self.final_states
        
        F = [i for i in range(len(self.states)) if i in finals]
        NF = [i for i in range(len(self.states)) if i not in finals]
        
        if F:  P.append(set(F))
        if NF: P.append(set(NF))
        
        changed = True
        while changed:
            changed = False
            new_partition = []
            for subset in P:
                if len(subset) <= 1:
                    # No hay nada que refinar
                    new_partition.append(subset)
                    continue
                # Tomar un estado representativo
                rep = next(iter(subset))
                # Agrupamos según la "signature"
                block_map = {}
                for q in subset:
                    signature = []
                    for a in self.alphabet:
                        # A dónde transiciona q con a
                        nxt = self.transitions.get((q, a), None)
                        # A qué bloque pertenece nxt
                        if nxt is None:
                            # Estado trampa
                            block_id = -1
                        else:
                            block_id = self._find_block(nxt, P)
                        signature.append((a, block_id))
                    signature.sort()
                    signature = tuple(signature)
                    
                    if signature not in block_map:
                        block_map[signature] = []
                    block_map[signature].append(q)
                
                # Cada key en block_map es una subdivisión
                for group in block_map.values():
                    new_partition.append(set(group))
                if len(block_map) > 1:
                    changed = True
            P = new_partition
        
        # Construir la versión minimizada
        self._build_min_dfa(P)

    def _find_block(self, state_id, partition):
        """
        Dado un state_id y la partición (lista de sets),
        retorna el índice del subconjunto al que pertenece state_id.
        """
        for i, block in enumerate(partition):
            if state_id in block:
                return i
        return -1
    
    def _build_min_dfa(self, partition):
        self.min_states = range(len(partition))
        self.min_transitions = {}
        self.min_final_states = set()
        
        # Mapeo de estado original -> bloque minimizado
        block_of = {}
        for i, block in enumerate(partition):
            for st in block:
                block_of[st] = i
        
        # El estado inicial en tu original dfa es ID 0 (asumiendo)
        # Buscamos a qué bloque pertenece
        self.min_start_state = block_of.get(0, 0)
        
        # Determinar los estados finales minimizados
        for i, block in enumerate(partition):
            if block & self.final_states:  # si hay intersección, es final
                self.min_final_states.add(i)
        
        # Construir transiciones
        for i, block in enumerate(partition):
            rep_state = next(iter(block))  # Tomamos un representante
            # Las transiciones del representante definen las del bloque
            for a in self.alphabet:
                nxt = self.transitions.get((rep_state, a))
                if nxt is not None or nxt not in block_of: # no existente o trampa
                    # b_id = block_of[nxt]
                    # self.min_transitions[(i, a)] = b_id
                    continue
                else:
                    target_block = block_of[nxt]
                    self.min_transitions[(i, a)] = target_block

    def get_minimized_dfa(self):
        return {
            "states": list(self.min_states),
            "transitions": self.min_transitions,
            "final_states": self.min_final_states,
            "start_state": self.min_start_state,
            "alphabet": self.alphabet
        }
    
    def visualize(self, filename="DFAA_graph"):
        print("Estados del DFAA min--:")
        for st_id, st_set in enumerate(self.states):
            is_final = (" (final)" if st_id in self.final_states else "")
            print(f"  S{st_id} = {set(st_set)}{is_final}")
        print("\nTransiciones:")
        for (sid, symbol), tid in self.transitions.items():
            print(f"  S{sid} -- {symbol} --> S{tid}")
