from dataclasses import dataclass
from typing import Set, Optional, List, Dict, FrozenSet
from parser.grammar import Grammar, Production, Symbol, NonTerminal, Terminal

@dataclass(frozen=True)
class Item:
    production: Production
    dot: int = 0

    def next_symbol(self) -> Optional[Symbol]:
        if self.dot < len(self.production.body):
            return self.production.body[self.dot]
        return None

    def advance_dot(self) -> "Item":
        if self.dot >= len(self.production.body):
            raise ValueError("No se puede avanzar más allá del final de la producción.")
        return Item(self.production, self.dot + 1)

    def __repr__(self) -> str:
        parts = list(self.production.body)
        parts.insert(self.dot, "·")
        return f"{self.production.head} → {' '.join(map(str, parts))}"


@dataclass(frozen=True)
class State:
    id: int
    items: FrozenSet[Item]

    def __repr__(self) -> str:
        lines = [f"State {self.id}:"]
        for it in sorted(self.items, key=lambda i: (str(i.production.head), i.dot)):
            lines.append(f"  {it}")
        return "\n".join(lines)


def closure(grammar: Grammar, items: Set[Item]) -> Set[Item]:
    prod_map: Dict[NonTerminal, List[Production]] = {}
    for p in grammar.productions:
        prod_map.setdefault(p.head, []).append(p)

    closure_set = set(items)
    changed = True
    while changed:
        changed = False
        for itm in list(closure_set):
            sym = itm.next_symbol()
            if isinstance(sym, NonTerminal):
                for p in prod_map[sym]:
                    new_it = Item(p, 0)
                    if new_it not in closure_set:
                        closure_set.add(new_it)
                        changed = True
    return closure_set


def goto(grammar: Grammar, items: Set[Item], symbol: Symbol) -> Set[Item]:
    moved = {itm.advance_dot() for itm in items if itm.next_symbol() == symbol}
    return closure(grammar, moved)


def build_canonical(grammar: Grammar) -> List[State]:
    aug = grammar.augmented()
    start_prod = aug.productions[0]  # S' → S
    start_item = Item(start_prod, 0)

    init_items = closure(aug, {start_item})
    init_state = State(0, frozenset(init_items))

    states: List[State] = [init_state]
    state_map: Dict[FrozenSet[Item], State] = {init_state.items: init_state}
    queue: List[State] = [init_state]
    next_id = 1

    while queue:
        st = queue.pop(0)
        # Generar símbolos en orden: primero terminales, luego no-terminales
        syms = {itm.next_symbol() for itm in st.items if itm.next_symbol() is not None}
        ordered_syms = sorted(
            syms,
            key=lambda s: (not isinstance(s, Terminal), str(s))
        )
        for sym in ordered_syms:
            new_items = goto(aug, set(st.items), sym)
            if not new_items:
                continue
            frozen = frozenset(new_items)
            if frozen not in state_map:
                new_st = State(next_id, frozen)
                states.append(new_st)
                state_map[frozen] = new_st
                queue.append(new_st)
                next_id += 1

    return states
