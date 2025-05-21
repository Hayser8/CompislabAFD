import re
from dataclasses import dataclass
from typing import Iterable, List

@dataclass(frozen=True)
class Tok:
    line:   int
    column: int
    type:   str
    lexeme: str

def remove_comments(text: str) -> List[str]:
    """
    Elimina comentarios multilínea de dos estilos:
      - C-style    /* ... */
      - OCaml-style (* ... *)
    Soporta anidamiento y reemplaza todo el contenido
    del comentario por espacios para no descolocar columnas.
    """
    lines = text.splitlines()
    output: List[str] = []
    in_c = 0
    in_ocaml = 0

    for raw in lines:
        chars = list(raw)
        i = 0
        while i < len(chars):
            # inicio C-style
            if i+1 < len(chars) and chars[i] == '/' and chars[i+1] == '*' and in_ocaml == 0:
                in_c += 1
                chars[i] = chars[i+1] = ' '
                i += 2
                continue
            # fin C-style
            if in_c > 0:
                if i+1 < len(chars) and chars[i] == '*' and chars[i+1] == '/':
                    in_c -= 1
                    chars[i] = chars[i+1] = ' '
                    i += 2
                else:
                    chars[i] = ' '
                    i += 1
                continue
            # inicio OCaml-style
            if i+1 < len(chars) and chars[i] == '(' and chars[i+1] == '*' and in_c == 0:
                in_ocaml += 1
                chars[i] = chars[i+1] = ' '
                i += 2
                continue
            # fin OCaml-style
            if in_ocaml > 0:
                if i+1 < len(chars) and chars[i] == '*' and chars[i+1] == ')':
                    in_ocaml -= 1
                    chars[i] = chars[i+1] = ' '
                    i += 2
                else:
                    chars[i] = ' '
                    i += 1
                continue
            # normal
            i += 1

        output.append("".join(chars))
    return output

def tokenize(text: str) -> Iterable[Tok]:
    """
    Tokeniza un fichero .yalp:
      - %token             → PERCENT_TOKEN
      - %%                 → PERCENT_PERCENT
      - IGNORE ident       → IGNORE
      - símbolos únicos: :, |, ;, (, ), ?, *, +
      - IDENTIFIER         → [_A-Za-z][_A-Za-z0-9]*
    """
    tokens: List[Tok] = []
    raw_lines   = text.splitlines()
    clean_lines = remove_comments(text)

    for lineno, line in enumerate(clean_lines, start=1):
        if not line.strip():
            continue

        # %token ...
        m = re.match(r'\s*%token\b', line)
        if m:
            col = m.start() + 1
            tokens.append(Tok(lineno, col, "PERCENT_TOKEN", "%token"))
            rest = line[m.end():]
            for idm in re.finditer(r'\b[A-Z_][A-Z0-9_]*\b', rest):
                tok = idm.group()
                tokens.append(Tok(lineno, m.end() + idm.start() + 1, "IDENTIFIER", tok))
            continue

        # %% delimiter
        if re.match(r'\s*%%\s*$', line):
            pos = line.find("%%")
            tokens.append(Tok(lineno, pos+1, "PERCENT_PERCENT", "%%"))
            continue

        # resto: símbolo a símbolo
        i = 0
        while i < len(line):
            ch = line[i]
            if ch.isspace():
                i += 1
                continue

            # un solo carácter de EBNF/producción
            if ch in {":", "|", ";", "(", ")", "?", "*", "+"}:
                tokens.append(Tok(lineno, i+1, ch, ch))
                i += 1
                continue

            # identificador (no-terminal o terminal)
            if ch.isalpha() or ch == "_":
                start = i
                while i < len(line) and (line[i].isalnum() or line[i] == "_"):
                    i += 1
                lex = line[start:i]
                typ = "IGNORE" if lex == "IGNORE" else "IDENTIFIER"
                tokens.append(Tok(lineno, start+1, typ, lex))
                continue

            raise SyntaxError(f"Carácter inesperado '{ch}' en línea {lineno}, columna {i+1}")

    return tokens
