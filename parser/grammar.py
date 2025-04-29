from dataclasses import dataclass
from typing import Set, Tuple, List, Union

# ──────────────────────── Clases de símbolos ────────────────────────

@dataclass(frozen=True)
class Terminal:
    """Representa un símbolo terminal."""
    name: str

    def __repr__(self):
        return self.name

@dataclass(frozen=True)
class NonTerminal:
    """Representa un símbolo no-terminal."""
    name: str

    def __repr__(self):
        return self.name

Symbol = Union[Terminal, NonTerminal]

# ──────────────────────── Clase de producción ────────────────────────

@dataclass(frozen=True)
class Production:
    """Representa una producción: head -> body."""
    id: int
    head: str
    body: Tuple[Symbol, ...]  # <-- AHORA ES UNA TUPLA

    def __repr__(self):
        body_str = " ".join(map(str, self.body))
        return f"{self.head} → {body_str}"

# ──────────────────────── Clase principal Grammar ────────────────────────

class Grammar:
    def __init__(self,
                 terminals: Set[Terminal],
                 non_terminals: Set[NonTerminal],
                 productions: List[Production],
                 start_symbol: NonTerminal):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def augmented(self) -> 'Grammar':
        """
        Devuelve una gramática aumentada (agrega S' -> S).
        """
        new_start_name = self.start_symbol.name + "'"
        augmented_start = NonTerminal(new_start_name)
        new_production = Production(
            id=-1,
            head=new_start_name,
            body=(self.start_symbol,)  # <-- también aquí usamos tupla
        )

        return Grammar(
            terminals=self.terminals,
            non_terminals=self.non_terminals.union({augmented_start}),
            productions=[new_production] + self.productions,
            start_symbol=augmented_start
        )

    def __repr__(self):
        return (
            f"Terminals: {self.terminals}\n"
            f"NonTerminals: {self.non_terminals}\n"
            f"Start Symbol: {self.start_symbol}\n"
            f"Productions:\n" +
            "\n".join(f"  {p}" for p in self.productions)
        )
