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
    head: NonTerminal
    body: Tuple[Symbol, ...]

    def __repr__(self):
        body_str = " ".join(map(str, self.body))
        return f"{self.head} → {body_str}"


# ──────────────────────── Clase principal Grammar ────────────────────────

class Grammar:
    """
    Modela una gramática libre de contexto:
    - terminals: símbolos terminales
    - non_terminals: símbolos no terminales
    - productions: lista de Production(head ∈ non_terminals, body ∈ (Symbol, ...))
    - start_symbol: símbolo de arranque
    """
    def __init__(self,
                 terminals: Set[Terminal],
                 non_terminals: Set[NonTerminal],
                 productions: List[Production],
                 start_symbol: NonTerminal):
        if start_symbol not in non_terminals:
            raise ValueError(f"Start symbol {start_symbol} debe estar en non_terminals")
        self._terminals = set(terminals)
        self._non_terminals = set(non_terminals)
        self.productions = list(productions)
        self.start_symbol = start_symbol

    @property
    def terminals(self) -> Set[Terminal]:
        return set(self._terminals)

    @property
    def non_terminals(self) -> Set[NonTerminal]:
        return set(self._non_terminals)

    def augmented(self) -> 'Grammar':
        """
        Devuelve una gramática aumentada (agrega S' → S) de forma idempotente:
        si el símbolo de inicio ya acaba en ', no la aumenta de nuevo.
        """
        # Si ya está aumentada (p.ej. start_symbol == "S'" o "X'" ...)
        if self.start_symbol.name.endswith("'"):
            return self

        # Sino, creamos una sola vez S' → S
        new_start = NonTerminal(self.start_symbol.name + "'")
        new_prod  = Production(
            id=-1,
            head=new_start,
            body=(self.start_symbol,),
        )

        return Grammar(
            terminals=self._terminals,
            non_terminals=self._non_terminals | {new_start},
            productions=[new_prod] + self.productions,
            start_symbol=new_start
        )

    def __repr__(self):
        lines = [
            f"Terminals: {{{', '.join(map(str, sorted(self._terminals, key=lambda t: t.name)))}}}",
            f"NonTerminals: {{{', '.join(map(str, sorted(self._non_terminals, key=lambda nt: nt.name)))}}}",
            f"Start Symbol: {self.start_symbol}",
            "Productions:"
        ]
        lines.extend(f"  {p}" for p in self.productions)
        return "\n".join(lines)


# ──────────────────────── Singleton ε ────────────────────────

# Usado para producciones vacías y cálculos FIRST/FOLLOW sin duplicar instancias
EPSILON = Terminal("ε")
