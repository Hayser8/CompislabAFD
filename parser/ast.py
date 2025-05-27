from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Tuple

@dataclass(frozen=True)
class ASTNode:
    """
    Nodo genérico de un Árbol de Sintaxis Abstracta (AST).
    
    :param name: etiqueta del nodo (p.ej. nombre de producción o tipo de operador)
    :param value: valor asociado (p.ej. número literal, nombre de identificador)
    :param children: tupla de ASTNode hijos
    """
    name: str
    value: Any = None
    children: Tuple[ASTNode, ...] = field(default_factory=tuple)

    def __repr__(self) -> str:
        # Representación estilo Lisp: (name [value] [child1] [child2] ...)
        parts: list[str] = []
        if self.value is not None:
            parts.append(repr(self.value))
        for c in self.children:
            parts.append(repr(c))
        if parts:
            return f"({self.name} " + " ".join(parts) + ")"
        else:
            return f"({self.name})"
