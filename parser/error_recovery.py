# parser/error_recovery.py

from typing import List
from parser.grammar import Terminal

# Tokens que consideramos “puntos de resynchronization”
SYNC_TOKENS = {"SEMICOLON", "RBRACE", "RPAREN"}

def panic_recover(state_stack: List[int],
                  symbol_stack: List,
                  ast_stack: List,
                  input_terms: List[Terminal],
                  index: int) -> int:
    """
    Descarta tokens desde `index` hasta encontrar un token
    cuya .name esté en SYNC_TOKENS o hasta '$'. Luego consume
    ese token sincronizador y retorna el nuevo índice.
    También reinicia las pilas (excepto el estado inicial).
    """
    # Vaciar stacks a estado inicial para reiniciar parseo
    state_stack[:] = [0]
    symbol_stack.clear()
    ast_stack.clear()

    # Saltar hasta sincronizador
    while index < len(input_terms):
        name = input_terms[index].name
        if name in SYNC_TOKENS or name == "$":
            break
        index += 1

    # Consumir el token sincronizador (salvo si es $)
    if index < len(input_terms) and input_terms[index].name in SYNC_TOKENS:
        index += 1

    return index
