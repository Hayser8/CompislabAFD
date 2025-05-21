# first_follow.py

from typing import Dict, Set, Union, List
from parser.grammar import Grammar, Terminal, NonTerminal, Symbol, EPSILON

class FirstFollowCalculator:
    """
    Calcula los conjuntos FIRST y FOLLOW para una gramática libre de contexto.
    """
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.first: Dict[Union[Terminal, NonTerminal], Set[Terminal]] = {}
        self.follow: Dict[NonTerminal, Set[Terminal]] = {}
        self.EPSILON = EPSILON
        self._compute_first()
        self._compute_follow()

    def _compute_first(self):
        # Inicialización: FIRST(t) = {t}, FIRST(nt) = ∅
        for t in self.grammar.terminals:
            self.first[t] = {t}
        for nt in self.grammar.non_terminals:
            self.first[nt] = set()
        # Asegurar que ε también esté en el diccionario
        self.first[self.EPSILON] = {self.EPSILON}

        changed = True
        while changed:
            changed = False
            for prod in self.grammar.productions:
                head: NonTerminal = prod.head
                before = len(self.first[head])
                first_body = self._first_of_sequence(list(prod.body))

                # Agregar todo excepto ε
                self.first[head].update(first_body - {self.EPSILON})
                # Si la secuencia genera ε, incluirlo
                if self.EPSILON in first_body:
                    self.first[head].add(self.EPSILON)

                if len(self.first[head]) > before:
                    changed = True

    def _first_of_sequence(self, seq: List[Symbol]) -> Set[Terminal]:
        if not seq:
            return {self.EPSILON}
        result: Set[Terminal] = set()
        for sym in seq:
            # Aquí `sym` puede ser T, NT, o EPSILON
            sym_first = self.first.get(sym, {self.EPSILON} if sym == self.EPSILON else set())
            result.update(sym_first - {self.EPSILON})
            if self.EPSILON not in sym_first:
                break
        else:
            # Todos generaron ε
            result.add(self.EPSILON)
        return result

    def _compute_follow(self):
        # Inicialización: FOLLOW(nt) = ∅
        for nt in self.grammar.non_terminals:
            self.follow[nt] = set()
        # El símbolo inicial lleva $
        self.follow[self.grammar.start_symbol].add(Terminal('$'))

        changed = True
        while changed:
            changed = False
            for prod in self.grammar.productions:
                head = prod.head
                trailer = set(self.follow[head])
                # Recorre de derecha a izquierda
                for sym in reversed(prod.body):
                    if isinstance(sym, NonTerminal):
                        before = len(self.follow[sym])
                        self.follow[sym].update(trailer)
                        if self.EPSILON in self.first[sym]:
                            trailer |= (self.first[sym] - {self.EPSILON})
                        else:
                            trailer = set(self.first[sym])
                        if len(self.follow[sym]) > before:
                            changed = True
                    else:
                        trailer = set(self.first.get(sym, set()))

    def get_first(self, sym: Symbol) -> Set[Terminal]:
        return self.first.get(sym, set())

    def get_follow(self, nt: NonTerminal) -> Set[Terminal]:
        return self.follow.get(nt, set())
