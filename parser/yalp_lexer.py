import re
from dataclasses import dataclass
from typing import Iterable, List

@dataclass
class Tok:
    line: int
    column: int
    type: str
    lexeme: str

def tokenize(text: str) -> Iterable[Tok]:
    tokens: List[Tok] = []
    lines = text.splitlines()
    line_number = 1
    in_comment = False

    for raw_line in lines:
        current_line = raw_line
        col_offset = 1

        # ───────────── Ignorar comentarios multilínea ─────────────
        if in_comment:
            if "*/" in current_line:
                in_comment = False
                current_line = current_line.split("*/", 1)[1]
            else:
                line_number += 1
                continue
        if "/*" in current_line:
            if "*/" in current_line:
                before, after = current_line.split("/*", 1)
                after = after.split("*/", 1)[1]
                current_line = before + after
            else:
                in_comment = True
                current_line = current_line.split("/*", 1)[0]

        line = current_line.strip()
        if not line:
            line_number += 1
            continue

        # ───────────── Detectar %token y sus identificadores ─────────────
        if line.startswith("%token"):
            col = current_line.find("%token") + 1
            tokens.append(Tok(line_number, col, "PERCENT_TOKEN", "%token"))

            rest = line[len("%token"):].strip()
            for match in re.finditer(r"[A-Z_][A-Z0-9_]*", rest):
                tok = match.group()
                start_col = current_line.find(tok, col) + 1
                tokens.append(Tok(line_number, start_col, "IDENTIFIER", tok))

            line_number += 1
            continue

        # ───────────── Detectar separador de secciones ─────────────
        if line.strip() == "%%":
            col = current_line.find("%%") + 1
            tokens.append(Tok(line_number, col, "PERCENT_PERCENT", "%%"))
            line_number += 1
            continue
        # ───────────── Detectar IGNORE y su identificador ─────────────
        if line.startswith("IGNORE"):
            col = current_line.find("IGNORE") + 1
            tokens.append(Tok(line_number, col, "IGNORE", "IGNORE"))

            rest = line[len("IGNORE"):].strip()
            match = re.match(r"[A-Z_][A-Z0-9_]*", rest)
            if match:
                tok = match.group()
                start_col = current_line.find(tok, col) + 1
                tokens.append(Tok(line_number, start_col, "IDENTIFIER", tok))
            else:
                raise SyntaxError(f"Se esperaba un identificador después de IGNORE en la línea {line_number}")

            line_number += 1
            continue
        # ───────────── Detectar producción o símbolos individuales ─────────────
        # Procesar el resto de la línea símbolo por símbolo
        i = 0
        while i < len(current_line):
            ch = current_line[i]

            # Saltar espacios
            if ch.isspace():
                i += 1
                continue

            # Símbolos especiales
            if ch in {":", "|", ";"}:
                tokens.append(Tok(line_number, i+1, ch, ch))
                i += 1
                continue

            # Identificadores (no terminales o tokens en producción)
            if ch.isalpha() or ch == "_":
                start = i
                while i < len(current_line) and (current_line[i].isalnum() or current_line[i] == "_"):
                    i += 1
                lexeme = current_line[start:i]
                tokens.append(Tok(line_number, start+1, "IDENTIFIER", lexeme))
                continue

            # Caracter desconocido
            raise SyntaxError(f"Carácter inesperado '{ch}' en la línea {line_number}, columna {i+1}")
        line_number += 1

    return tokens
