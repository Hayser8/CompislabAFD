from typing import List, Set, Optional
from grammar import Grammar, Production, Symbol, NonTerminal, Terminal

class Item:
    def __init__(self, production: Production, dot: int = 0):
        self.production = production
        self.dot = dot

    def next_symbol(self) -> Optional[Symbol]:
        if self.dot < len(self.production.body):
            return self.production.body[self.dot]
        return None

    def advance_dot(self) -> 'Item':
        if self.dot >= len(self.production.body):
            raise ValueError("No se puede avanzar más allá del final de la producción.")
        return Item(self.production, self.dot + 1)

    def __eq__(self, other):
        return isinstance(other, Item) and self.production == other.production and self.dot == other.dot

    def __hash__(self):
        return hash((self.production, self.dot))

    def __repr__(self):
        body = list(self.production.body)
        body.insert(self.dot, '·')
        return f"{self.production.head} → {' '.join(map(str, body))}"

class State:
    def __init__(self, id: int, items: Set[Item]):
        self.id = id
        self.items = frozenset(items)

    def __eq__(self, other):
        return isinstance(other, State) and self.items == other.items

    def __hash__(self):
        return hash(self.items)

    def __repr__(self):
        items_str = '\n'.join(f"  {repr(item)}" for item in sorted(self.items, key=lambda x: (str(x.production.head), x.dot)))
        return f"State {self.id}:\n{items_str}"

def closure(grammar: Grammar, items: Set[Item]) -> Set[Item]:
    closure_set = set(items)
    changed = True
    while changed:
        changed = False
        new_items = set()
        for item in closure_set:
            next_sym = item.next_symbol()
            if isinstance(next_sym, NonTerminal):
                for prod in grammar.productions:
                    if prod.head == next_sym:
                        new_item = Item(prod, 0)
                        if new_item not in closure_set:
                            new_items.add(new_item)
        if new_items:
            closure_set.update(new_items)
            changed = True
    return closure_set

def goto(grammar: Grammar, items: Set[Item], symbol: Symbol) -> Set[Item]:
    moved = set()
    for item in items:
        if item.next_symbol() == symbol:
            moved.add(item.advance_dot())
    return closure(grammar, moved)

def build_canonical(grammar: Grammar) -> List[State]:
    states: List[State] = []
    augmented = grammar.augmented()

    start_prod = Production(
        id=-1,
        head=augmented.start_symbol,
        body=(grammar.start_symbol,)  # ← CAMBIO CRÍTICO
    )

    initial_item = Item(start_prod, 0)
    initial_closure = closure(augmented, {initial_item})
    initial_state = State(0, initial_closure)
    states.append(initial_state)

    queue = [initial_state]
    next_id = 1

    while queue:
        current = queue.pop(0)
        symbols = {item.next_symbol() for item in current.items if item.next_symbol() is not None}
        for sym in symbols:
            goto_items = goto(augmented, current.items, sym)
            if not goto_items:
                continue
            for st in states:
                if st.items == goto_items:
                    break
            else:
                new_state = State(next_id, goto_items)
                states.append(new_state)
                queue.append(new_state)
                next_id += 1

    return states
