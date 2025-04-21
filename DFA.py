# DFA.py
from typing import Dict, FrozenSet, Optional
from graphviz import Digraph
from arbolSINT import SyntaxTree                    # tu clase SyntaxTree


# ----------------------------------------------------------------------
def _esc(lbl: str) -> str:
    """Escapa texto para Graphviz."""
    return (
        lbl.replace("\\", "\\\\")
           .replace('"',  r"\"")
           .replace("{", r"\{")
           .replace("}", r"\}")
    )


def _is_marker(sym: str, marker_map: Dict[str, str]) -> bool:
    """
    Devuelve True si el símbolo `sym` es un marcador de fin de expresión.
    • Puede venir como '__EOF_7__'  (cuando lo miramos en marker_map)
    • o como 'LIT<<__EOF_7__>>'    (cuando procede del árbol).
    """
    if sym in marker_map:
        return True
    return "__EOF_" in sym      # coincide incluso con 'LIT<<__EOF_7__>>'


# ----------------------------------------------------------------------
class DFA:
    """
    DFA directo (Aho–Sethi–Ullman) **sin** símbolo EOF adicional.
    Un estado es final si contiene al menos una posición cuyo símbolo sea
    un marcador __EOF_i__ (en cualquiera de sus dos variantes mencionadas).
    """

    # ------------------------------------------------------------------
    def __init__(self,
                 syntax_tree: SyntaxTree,
                 marker_map: Optional[Dict[str, str]] = None):

        self.marker_map: Dict[str, str] = marker_map or {}

        # ---- estructuras auxiliares ----------------------------------
        self.followpos: Dict[int, set[int]] = {}
        self.pos_to_symbol: Dict[int, str]  = {}

        # ---- paso 1: nullable / firstpos / lastpos + followpos -------
        pos_ctr = [1]                             # contador incremental
        self.nullable, self.firstpos, self.lastpos = self._functions(
            syntax_tree.root,
            self.followpos,
            self.pos_to_symbol,
            pos_ctr
        )

        # ---- paso 2: construcción del DFA ----------------------------
        self.start_state: FrozenSet[int] = frozenset(self.firstpos)

        # ① Posiciones que contienen marcadores  -----------------------
        self.marker_positions = {
            p for p, s in self.pos_to_symbol.items()
            if _is_marker(s, self.marker_map)
        }

        self.transitions: Dict[FrozenSet[int], Dict[str, FrozenSet[int]]] = {}
        self.final_states: set[FrozenSet[int]] = set()
        self._build()

        # ② Mapeo estado → acción --------------------------------------
        self.state_actions: Dict[FrozenSet[int], str] = {}
        for st in self.final_states:
            for p in st:
                sym = self.pos_to_symbol[p]
                if sym in self.marker_map:
                    self.state_actions[st] = self.marker_map[sym]
                    break
                if _is_marker(sym, self.marker_map):
                    self.state_actions[st] = "ACCEPT"
                    break

    # ==================================================================
    # ==========  MÉTODOS PRIVADOS  ====================================
    # ==================================================================

    # -- funciones auxiliares del algoritmo directo --------------------
    def _functions(self, node, followpos, pos_to_symbol, pos_counter):
        if node.left is None and node.right is None:          # hoja
            if node.value == 'ε':
                return True, set(), set()

            pos = pos_counter[0]
            pos_counter[0] += 1
            node.pos = pos
            pos_to_symbol[pos] = node.value
            return False, {pos}, {pos}

        if node.value == '|':
            ln, lf, ll = self._functions(node.left,  followpos,
                                         pos_to_symbol, pos_counter)
            rn, rf, rl = self._functions(node.right, followpos,
                                         pos_to_symbol, pos_counter)
            return ln or rn, lf | rf, ll | rl

        if node.value == '·':
            ln, lf, ll = self._functions(node.left,  followpos,
                                         pos_to_symbol, pos_counter)
            rn, rf, rl = self._functions(node.right, followpos,
                                         pos_to_symbol, pos_counter)
            for p in ll:
                followpos.setdefault(p, set()).update(rf)
            first = lf | rf if ln else lf
            last  = ll | rl if rn else rl
            return ln and rn, first, last

        if node.value == '*':
            cn, cf, cl = self._functions(node.left, followpos,
                                         pos_to_symbol, pos_counter)
            for p in cl:
                followpos.setdefault(p, set()).update(cf)
            return True, cf, cl

        raise ValueError(f"Operador no soportado: {node.value}")

    # -- construcción de estados y transiciones ------------------------
    def _build(self):
        worklist = [self.start_state]
        seen     = {self.start_state}

        while worklist:
            S = worklist.pop()
            self.transitions[S] = {}

            buckets: Dict[str, set[int]] = {}
            for p in S:
                sym = self.pos_to_symbol[p]
                if _is_marker(sym, self.marker_map) or sym == 'ε':
                    continue                           # no genera transición
                buckets.setdefault(sym, set()).update(self.followpos.get(p, set()))

            for a, tgt in buckets.items():
                T = frozenset(tgt)
                self.transitions[S][a] = T
                if T not in seen:
                    seen.add(T)
                    worklist.append(T)

        # estados finales = los que contienen al menos un marcador
        self.final_states = {st for st in seen if st & self.marker_positions}

    # -- visualización opcional ----------------------------------------
    def visualize(self, filename: str = "dfa"):
        dot, ids, n = Digraph("DFA"), {}, 0

        for st in self.transitions:
            ids[st] = f"S{n}"; n += 1
        for st in self.final_states - self.transitions.keys():
            ids[st] = f"S{n}"; n += 1

        for st, node_id in ids.items():
            shape = "doublecircle" if st in self.final_states else "circle"
            dot.node(node_id, _esc(str(set(st))), shape=shape)

        dot.node("start", shape="none", label="")
        dot.edge("start", ids[self.start_state])

        for src, trans in self.transitions.items():
            for a, dst in trans.items():
                dot.edge(ids[src], ids[dst], label=_esc(a))

        dot.render(filename, format="png", cleanup=True)
        print("DFA image saved:", filename + ".png")
