from typing import Dict, Set, Union
from grammar import Grammar, Terminal, NonTerminal, Symbol

class FirstFollowCalculator:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.first: Dict[Union[Terminal, NonTerminal], Set[Terminal]] = {}
        self.follow: Dict[NonTerminal, Set[Terminal]] = {}
        self.EPSILON = Terminal("ε")  # usamos un Terminal especial para ε

        self._compute_first()
        self._compute_follow()

    def _compute_first(self):
        """Calcula todos los conjuntos FIRST."""
        # Inicialización
        for t in self.grammar.terminals:
            self.first[t] = {t}
        for nt in self.grammar.non_terminals:
            self.first[nt] = set()

        changed = True
        while changed:
            changed = False
            for production in self.grammar.productions:
                # ❗️ production.head ahora es str, buscamos el NonTerminal real
                head = next(nt for nt in self.grammar.non_terminals if str(nt) == production.head)
                body = production.body
                before = len(self.first[head])

                first_body = self._first_of_sequence(body)
                self.first[head].update(first_body - {self.EPSILON})

                if self.EPSILON in first_body:
                    self.first[head].add(self.EPSILON)

                if len(self.first[head]) > before:
                    changed = True

    def _first_of_sequence(self, sequence: list[Symbol]) -> Set[Terminal]:
        """Calcula FIRST de una secuencia de símbolos."""
        if not sequence:
            return {self.EPSILON}

        first_set = set()
        for symbol in sequence:
            first_symbol = self.first[symbol]
            first_set.update(first_symbol - {self.EPSILON})
            if self.EPSILON not in first_symbol:
                break
        else:
            first_set.add(self.EPSILON)

        return first_set

    def _compute_follow(self):
        """Calcula todos los conjuntos FOLLOW."""
        # Inicialización
        for nt in self.grammar.non_terminals:
            self.follow[nt] = set()

        # El símbolo inicial contiene $
        self.follow[self.grammar.start_symbol].add(Terminal('$'))

        changed = True
        while changed:
            changed = False
            for production in self.grammar.productions:
                head = next(nt for nt in self.grammar.non_terminals if str(nt) == production.head)
                body = production.body
                trailer = self.follow[head].copy()

                for symbol in reversed(body):
                    if isinstance(symbol, NonTerminal):
                        before = len(self.follow[symbol])
                        self.follow[symbol].update(trailer)

                        if self.EPSILON in self.first[symbol]:
                            trailer.update(self.first[symbol] - {self.EPSILON})
                        else:
                            trailer = self.first[symbol]

                        if len(self.follow[symbol]) > before:
                            changed = True
                    else:
                        trailer = self.first[symbol]

    def get_first(self, symbol: Symbol) -> Set[Terminal]:
        return self.first.get(symbol, set())

    def get_follow(self, non_terminal: NonTerminal) -> Set[Terminal]:
        return self.follow.get(non_terminal, set())

    def dump_first(self):
        print("=== FIRST sets ===")
        for symbol, first_set in self.first.items():
            if isinstance(symbol, NonTerminal):
                print(f"FIRST({symbol}) = {{{', '.join(map(str, first_set))}}}")

    def dump_follow(self):
        print("=== FOLLOW sets ===")
        for symbol, follow_set in self.follow.items():
            print(f"FOLLOW({symbol}) = {{{', '.join(map(str, follow_set))}}}")
