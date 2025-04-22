# MinimizedDFA.py
from __future__ import annotations

from DFA import DFA
from graphviz import Digraph

# ------------------------------------------------------------
def _esc(lbl: str) -> str:
    """Escapa los caracteres problemáticos para Graphviz."""
    return (
        lbl.replace("\\", "\\\\")
           .replace('"',  r"\"")
           .replace("{", r"\{")
           .replace("}", r"\}")
    )


class MinimizedDFA:
    """
    Minimiza un DFA (Aho‑Sethi‑Ullman → Hopcroft).

    *   NO depende de que el DFA original use símbolo «EOF».
    *   Mantiene un mapa `state_actions` con la acción léxica asociada
        a cada estado del DFA minimizado.
    """

    # --------------------------------------------------------
    def __init__(self, dfa: DFA) -> None:
        # --- referencia al DFA original ---------------------
        self.original_dfa: DFA = dfa          # <- la conservamos
        self.start_state       = dfa.start_state
        self.transitions       = dfa.transitions
        self.final_states      = set(dfa.final_states)
        self.states            = self._reachable()

        # -------- Partición inicial P = { F , Q \ F } -------
        finals = self.final_states
        nonf   = self.states - finals
        P      = [b for b in (finals, nonf) if b]   # sin conjuntos vacíos
        W      = P.copy()                           # bloques pendientes

        # Alfabeto Σ
        alphabet = {a for q in self.states
                      for a in self.transitions.get(q, {})}

        # ---------------- Algoritmo de Hopcroft --------------
        while W:
            A = W.pop()
            for a in alphabet:
                pre = {q for q in self.states
                       if a in self.transitions.get(q, {}) and
                          self.transitions[q][a] in A}
                if not pre:
                    continue

                new_P, new_W = [], []
                for Y in P:
                    inter, diff = Y & pre, Y - pre
                    if inter and diff:
                        new_P.extend((inter, diff))
                        if Y in W:
                            W.remove(Y)
                            new_W.extend((inter, diff))
                        else:
                            # elige el bloque más pequeño para insertar en W
                            new_W.append(inter if len(inter) <= len(diff) else diff)
                    else:
                        new_P.append(Y)
                P, W = new_P, W + new_W

        # --------------- Construcción del DFA mínimo ---------
        self.minimized_states      = {frozenset(b) for b in P}
        self.minimized_final       = {frozenset(b) for b in P if b & self.final_states}
        self.minimized_start: frozenset[int] = next(
            frozenset(b) for b in P if self.start_state in b
        )

        # Transiciones
        self.minimized_transitions: dict[frozenset[int], dict[str, frozenset[int]]] = {
            st: {} for st in self.minimized_states
        }
        for block in P:
            rep   = next(iter(block))           # representante
            blk_f = frozenset(block)
            for a, tgt in self.transitions.get(rep, {}).items():
                tgt_blk = next(frozenset(b) for b in P if tgt in b)
                self.minimized_transitions[blk_f][a] = tgt_blk

        # --------- NUEVO: mapa estado_min → acción -----------
        # (necesario para el generador de código)
        self.state_actions: dict[frozenset[int], str] = {}
        for blk in self.minimized_states:
            for orig_state in blk:
                act = self.original_dfa.state_actions.get(orig_state)
                if act:                     # tomamos la primera acción encontrada
                    self.state_actions[blk] = act
                    break

    # --------------------------------------------------------
    def _reachable(self) -> set[frozenset[int]]:
        """Devuelve los estados alcanzables desde el estado inicial."""
        reach, work = {self.start_state}, [self.start_state]
        while work:
            q = work.pop()
            for nxt in self.transitions.get(q, {}).values():
                if nxt not in reach:
                    reach.add(nxt)
                    work.append(nxt)
        return reach

    # --------------------------------------------------------
    def visualize(self, filename: str = "min_dfa") -> None:
        """Genera un PNG del DFA minimizado usando Graphviz."""
        dot, ids, n = Digraph("MinDFA"), {}, 0
        for st in self.minimized_states:
            ids[st] = f"M{n}"
            n += 1
            shape = "doublecircle" if st in self.minimized_final else "circle"
            lbl   = "{" + ", ".join(map(str, sorted(st))) + "}"
            dot.node(ids[st], _esc(lbl), shape=shape)

        dot.node("start", shape="none", label="")
        dot.edge("start", ids[self.minimized_start])

        for src, trans in self.minimized_transitions.items():
            for a, dst in trans.items():
                dot.edge(ids[src], ids[dst], label=_esc(a))

        dot.render(filename, format="png", cleanup=True)
        print("Minimized DFA image saved:", filename + ".png")
