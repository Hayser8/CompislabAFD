# parser_table.py

from typing import Dict, Tuple
from parser.grammar import Grammar, Terminal, NonTerminal
from parser.first_follow import FirstFollowCalculator
from parser.lr0 import build_canonical, goto

Action = Tuple[str, int]  
# 's' = shift a estado, 'r' = reduce por producción, 'acc' = accept

def build_slr_table(grammar: Grammar) -> Tuple[Dict[Tuple[int, Terminal], Action],
                                               Dict[Tuple[int, NonTerminal], int]]:
    """
    Construye las tablas ACTION y GOTO para un parser SLR(1).

    Returns:
      - action[(state_id, terminal)] = ('s', j) o ('r', prod_id) o ('acc', 0)
      - goto[(state_id, non_terminal)] = nuevo_estado
    """
    # 1) Gramática aumentada y autómata LR(0)
    aug = grammar.augmented()
    states = build_canonical(grammar)
    # Mapping de items->state_id para lookup rápido
    items_to_id = {st.items: st.id for st in states}

    # 2) FIRST/FOLLOW de la gramática original
    ff = FirstFollowCalculator(grammar)

    action: Dict[Tuple[int, Terminal], Action] = {}
    goto_table: Dict[Tuple[int, NonTerminal], int] = {}

    for st in states:
        for item in st.items:
            a = item.next_symbol()
            # 2a) SHIFT: si 'a' es terminal, desplazamos y cerramos
            if isinstance(a, Terminal):
                j_items = goto(aug, set(st.items), a)
                if j_items:
                    j = items_to_id[frozenset(j_items)]
                    action[(st.id, a)] = ('s', j)
            # 2b) REDUCE or ACCEPT: si punto al final
            elif a is None:
                prod = item.production
                if prod.id == -1:
                    # producción aumentada S'→S· → accept en $
                    action[(st.id, Terminal('$'))] = ('acc', 0)
                else:
                    # reduce por prod.id en cada b ∈ FOLLOW(head)
                    for b in ff.get_follow(prod.head):
                        action[(st.id, b)] = ('r', prod.id)

        # 3) GOTO: transiciones por no-terminales
        for A in grammar.non_terminals:
            j_items = goto(aug, set(st.items), A)
            if j_items:
                j = items_to_id[frozenset(j_items)]
                goto_table[(st.id, A)] = j

    return action, goto_table
