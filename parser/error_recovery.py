# parser/error_recovery.py

from typing import List
from parser.grammar import Terminal

# Tokens de sincronización
SYNC_TOKENS = {"SEMICOLON", "RBRACE", "RPAREN"}

def panic_recover(state_stack: List[int],
                  symbol_stack: List,
                  ast_stack: List,
                  input_terms: List[Terminal],
                  index: int) -> int:
    """
    Modo pánico: limpia pilas y salta hasta un token de sincronización o '$'.
    Evita loops infinitos si no se encuentra ninguno.
    """
    print(f"[RECOVERY] Iniciando recuperación en index={index}")

    # Reiniciar pilas
    state_stack[:] = [0]
    symbol_stack.clear()
    ast_stack.clear()

    # Buscar token de sincronización
    while index < len(input_terms):
        name = input_terms[index].name
        if name in SYNC_TOKENS or name == "$":
            break
        index += 1

    # Si encuentra token sincronizador, consumirlo
    if index < len(input_terms):
        if input_terms[index].name in SYNC_TOKENS:
            print(f"[RECOVERY] Token sincronizador encontrado: {input_terms[index].name}")
            index += 1
        elif input_terms[index].name == "$":
            print(f"[RECOVERY] Fin de archivo alcanzado ($)")
            index += 1

    print(f"[RECOVERY] Reanudando desde index={index}")
    return index
