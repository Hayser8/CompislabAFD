from typing import List, Tuple, Optional
from parser.grammar import Grammar, Terminal, NonTerminal, Production, Symbol
from parser.parser_table import build_slr_table
from parser.error_recovery import panic_recover
from parser.ast import ASTNode  

class ParseError(Exception):
    """Error sintáctico indicando el estado y el token que falló."""
    def __init__(self, state: int, token: Symbol, message: str = "Unexpected token"):
        super().__init__(f"[PARSER] Estado {state}, token {token}: {message}")
        self.state = state
        self.token = token

class Parser:
    """
    Driver SLR(1) que, dada una gramática, construye ACTION/GOTO
    y provee `parse` con recuperación en modo pánico.
    """
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.action, self.goto = build_slr_table(grammar)

    def parse(self,
              tokens: List[Tuple[str, str]]
             ) -> Tuple[Optional[ASTNode], List[str]]:
        """
        :param tokens: Lista de pares (lexeme, token_type).
        :returns: (AST raíz o None si no pudo, lista de mensajes de error)
        """
        # Convertir token_type a Terminal e insertar marcador final '$'
        input_terms = [Terminal(t_type) for (_, t_type) in tokens] + [Terminal('$')]

        state_stack: List[int] = [0]
        symbol_stack: List[Symbol] = []
        ast_stack:    List[ASTNode] = []
        index = 0
        errors: List[str] = []

        while index < len(input_terms):
            state = state_stack[-1]
            lookahead = input_terms[index]
            act = self.action.get((state, lookahead))

            try:
                if act is None:
                    raise ParseError(state, lookahead)

                kind, val = act
                if kind == 's':  # shift
                    state_stack.append(val)
                    symbol_stack.append(lookahead)
                    # apilar leaf provisional en AST
                    ast_stack.append(ASTNode(str(lookahead), lookahead.name))
                    index += 1

                elif kind == 'r':  # reduce
                    prod: Production = self.grammar.productions[val]
                    # 1) extraer hijos AST
                    n = len(prod.body)
                    children = [ast_stack.pop() for _ in range(n)][::-1]
                    # 2) desencolar símbolos y estados
                    for _ in prod.body:
                        symbol_stack.pop()
                        state_stack.pop()
                    # 3) crear nodo semántico neutro
                    node = ASTNode(prod.head.name, None, tuple(children))
                    ast_stack.append(node)
                    # 4) push head y goto
                    symbol_stack.append(prod.head)
                    goto_state = self.goto.get((state_stack[-1], prod.head))
                    if goto_state is None:
                        raise ParseError(state_stack[-1], prod.head, "Missing GOTO")
                    state_stack.append(goto_state)

                elif kind == 'acc':  # accept
                    # terminado con éxito
                    root = ast_stack[0] if ast_stack else None
                    return root, errors

                else:
                    raise ParseError(state, lookahead, f"Unknown action {kind}")

            except ParseError as pe:
                errors.append(str(pe))
                # Recuperación en modo pánico
                index = panic_recover(state_stack,
                                      symbol_stack,
                                      ast_stack,
                                      input_terms,
                                      index)
                # seguimos parseando

        # Si salimos del bucle sin accept, es error
        errors.append("[PARSER] Fin de entrada inesperado")
        return None, errors
