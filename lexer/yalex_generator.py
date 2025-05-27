#!/usr/bin/env python3
# yalex_generator.py ─ genera «lexeitor.py» a partir de «lexer.yal»

import json
import sys
from yalex_pipeline import integrate_yalex_pipeline

def _clean_block(block: str) -> str:
    """Recorta las llaves sobrantes de los bloques header/trailer."""
    lines = block.splitlines()
    if lines and lines[0].strip() == "{":
        lines = lines[1:]
    if lines and lines[-1].strip() == "}":
        lines = lines[:-1]
    body = "\n".join(lines).rstrip()
    diff = body.count("{") - body.count("}")
    return body + ("\n" + "}" * diff if diff > 0 else "")

def generate_lexer_code(pipeline_result, out_file: str = "lexeitor.py"):
    header  = _clean_block(pipeline_result["header"])
    trailer = _clean_block(pipeline_result["trailer"])
    rules   = pipeline_result["rules"]

    if "gettoken" not in rules:
        raise KeyError('Regla principal "gettoken" no encontrada')

    dfa_alts = []
    for ix, entry in enumerate(rules["gettoken"]):
        mdfa = entry["min_dfa"]
        start = str(mdfa.minimized_start)
        finals = {str(s) for s in mdfa.minimized_final}
        st_actions = {
            str(st): act
            for st, act in getattr(mdfa, "state_actions", {}).items()
        }

        # Aseguramos que el comentario tenga su propia acción
        if entry["action"] == "COMMENT":
            st_actions[start] = "COMMENT"

        # Construimos la tabla de transiciones (incluyendo ":" y todo literal)
        trans = {}
        for st, tbl in mdfa.minimized_transitions.items():
            k = str(st)
            for sym, tgt in tbl.items():
                if sym.startswith("0:__EOF_"):
                    finals.add(k)
                    if str(tgt) in st_actions and k not in st_actions:
                        st_actions[k] = st_actions[str(tgt)]
                    continue
                trans.setdefault(k, {})[sym] = str(tgt)

        dfa_alts.append({
            "regex":           entry["regex"],
            "action":          entry["action"],
            "alternatives":    entry.get("alternatives", []),
            "dfa_transitions": trans,
            "dfa_start":       start,
            "dfa_final":       sorted(finals),
            "state_actions":   st_actions,
        })

    json_alts = json.dumps(dfa_alts, indent=4)

    runtime = r'''
import re, sys

class LexerError(Exception):
    """Errores durante el análisis léxico."""
    def __init__(self, msg, line, col):
        super().__init__(f"[LÉXICO] L{line}:C{col}: {msg}")
        self.line, self.column = line, col

def _strip_comments(text: str) -> str:
    # No eliminamos aquí; el DFA maneja '#' como token
    return text

def decode_robust_key(key: str):
    if key.startswith("LIT<<") and key.endswith(">>"):
        lit = key[5:-2]
        return False, len(lit), {lit}
    i = 0
    while i < len(key) and key[i].isdigit():
        i += 1
    if i and i < len(key) and key[i] == ":":
        body = key[i+1:]
        if body.startswith("(") and body.endswith(")"):
            return True, 1, set(body[1:-1].split("|"))
        return True, int(key[:i]), {body}
    if key.startswith(":"):
        lit = key[1:]
        if lit.startswith("(") and lit.endswith(")"):
            return True, 1, set(lit[1:-1].split("|"))
        return True, len(lit), {lit}
    return False, len(key), {key}

def simulate_dfa(dfa, text: str):
    state, best, pos = dfa["dfa_start"], ("", 0, None), 0
    while pos < len(text):
        chunk = text[pos:]
        matched = False
        for sym, tgt in dfa["dfa_transitions"].get(state, {}).items():
            is_set, ln, charset = decode_robust_key(sym)
            if ln > len(chunk): continue
            probe = chunk[:ln]
            if (probe in charset) if is_set else (probe == sym):
                state, pos, matched = tgt, pos + ln, True
                if state in dfa["dfa_final"]:
                    best = (text[:pos], pos, state)
                break
        if not matched:
            break
    return best if best[1] else (None, 0, None)

# ——— map de símbolos simples y compuestos ———
_token_map = {
    # simples
    "+":"PLUS", "-":"MINUS", "*":"TIMES", "/":"DIV", "%":"MODULO",
    "=":"ASSIGN", "<":"LT", ">":"GT", ":":"COLON", ".":"DOT",
    ",":"COMMA", ";":"SEMICOLON", 
    "(":"LPAREN", ")":"RPAREN", "[":"LBRACKET", "]":"RBRACKET",
    "{":"LBRACE", "}":"RBRACE",
    # compuestos (elipsis primero)
    "...":"ELLIPSIS",
    "==":"EQ", "!=":"NE", "<=":"LE", ">=":"GE",
    ":=":"WALRUS", "->":"RARROW",
    "**":"POW", "//":"FLOORDIV",
    "+=":"PLUSEQ", "-=":"MINEQ", "*=":"TIMEQ",
    "/=":"DIVEQ", "%=":"MODEQ",
    "**=":"POW_EQ", "//=":"FLOORDIV_EQ",
}

# Reconoce bin, oct, hex, dec con underscores y floats con exponentes
_num = re.compile(r'^(?:0[bB][01_]+|0[oO][0-7_]+|0[xX][0-9A-Fa-f_]+|\d[\d_]*)$')
_flt = re.compile(r'^(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*[eE][+-]?\d[\d_]*)$')
_id  = re.compile(r'^[A-Za-z_][A-Za-z_0-9]*$')

def _categorize(lxm: str):
    if lxm in keywords:     return keywords[lxm]
    if lxm in _token_map:   return _token_map[lxm]
    if "\n" in lxm:         return "NEWLINE"
    if all(c.isspace() for c in lxm): return "WHITESPACE"
    if _flt.match(lxm):     return "FLOAT"
    if _num.match(lxm):     return "INTEGER"
    if _id.match(lxm):      return "IDENTIFIER"
    return "UNKNOWN"

_cur_line, _cur_col = 1, 1

def get_token(text: str):
    global _cur_line, _cur_col

    # 0) NEWLINE puro  ── ¡antes que nada!
    if text.startswith("\r\n"):
        return "\r\n", "NEWLINE", 2          # solo CRLF
    if text[0] == "\n":
        return "\n", "NEWLINE", 1            # solo LF

    # Comentario de línea con '#'
    if text.startswith("#"):
        idx = text.find("\n")
        if idx == -1: idx = len(text)
        return text[:idx], "COMMENT", idx

    # Literales de cadena
    if text[0] in {"'", '"'}:
        quote = text[0]
        if text.startswith(quote*3):
            end_seq = quote*3
            i = 3
            while i < len(text):
                if text.startswith(end_seq, i):
                    i += 3
                    return text[:i], "STRING", i
                if text[i] == "\\" and i+1 < len(text):
                    i += 2
                else:
                    i += 1
            raise LexerError("Cadena triple sin cerrar", _cur_line, _cur_col)
        i, esc = 1, False
        while i < len(text):
            if not esc and text[i] == quote:
                return text[:i+1], "STRING", i+1
            esc = (not esc and text[i] == "\\")
            i += 1
        raise LexerError("Cadena sin cerrar", _cur_line, _cur_col)

    # 1) Elipsis '...'
    if text.startswith("..."):
        return "...", "ELLIPSIS", 3

    # 2) Literales numéricas con prefijos 0b/0o/0x y underscores
    m = re.match(r'0[bB][01_]+|0[oO][0-7_]+|0[xX][0-9A-Fa-f_]+', text)
    if m:
        lit = m.group(0)
        return lit, "INTEGER", len(lit)
    
    if text.startswith(".") and len(text) > 1 and text[1].isdigit():
        j = 2
        while j < len(text) and text[j].isdigit():
            j += 1
        return text[:j], "FLOAT", j

    # 3) DFA unificado
    best_lx, best_ac, best_ln = None, None, 0
    for dfa in dfa_alternatives:
        lx, ln, st = simulate_dfa(dfa, text)
        if ln > best_ln:
            best_ln, best_lx = ln, lx
            best_ac = dfa["state_actions"].get(str(st)) or dfa["action"]
    
    # 4) Dos caracteres
    two = text[:2]
    if two in _token_map and best_ln < 2:
        return two, _token_map[two], 2

    # 5) Fallback manual
    if best_ln == 0 and text:
        ch = text[0]
        if ch in _token_map:
            return ch, _token_map[ch], 1
        if ch.isalpha() or ch == "_":
            j = 1
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            tok = text[:j]
            return tok, keywords.get(tok, "IDENTIFIER"), j
        if ch.isdigit():
            i = 0
            while i < len(text) and text[i].isdigit():
                i += 1
            if i < len(text) and text[i] == ".":
                j = i+1
                while j < len(text) and text[j].isdigit():
                    j += 1
                if j > i+1:
                    return text[:j], "FLOAT", j
            if i < len(text) and text[i] in "eE":
                j = i + 1
                if j < len(text) and text[j] in "+-":   # signo opcional
                    j += 1
                k = j
                while k < len(text) and text[k].isdigit():
                    k += 1
                if k > j:                               # al menos un dígito
                    return text[:k], "FLOAT", k
            return text[:i], "INTEGER", i

    # 6) Categorización final
    if best_ac in (None, "unified", "ACCEPT") and best_lx is not None:
        best_ac = _categorize(best_lx)

    if best_ln == 0:
       raise LexerError("Símbolo desconocido", _cur_line, _cur_col)

    return best_lx, best_ac, best_ln

def scan(text: str):
    pos = 0
    n = len(text)
    indent_stack = [0]
    out = []
    new_line = True
    cur_line, cur_col = 1, 1

    while pos < n:
        if new_line:
            # 1) detectar indent/dedent
            start = pos
            while pos < n and text[pos] == ' ':
                pos += 1
            indent = pos - start
            if indent > indent_stack[-1] and indent % 4 == 0:
                indent_stack.append(indent)
                out.append(("", "INDENT"))
            while indent < indent_stack[-1]:
                indent_stack.pop()
                out.append(("", "DEDENT"))
            new_line = False

        # 2) extraer siguiente token
        lexeme, tok, length = get_token(text[pos:])
        if length == 0:
            raise LexerError("Símbolo desconocido", cur_line, cur_col)

        # 3) actualizar línea/columna
        lines = lexeme.split('\n')
        if len(lines) > 1:
            cur_line += len(lines) - 1
            cur_col = len(lines[-1]) + 1
            new_line = (tok == "NEWLINE")
        else:
            cur_col += length

        pos += length

        # 4) filtrar comentarios y whitespace
        if tok not in {"COMMENT", "MULTILINE_COMMENT", "WHITESPACE"}:
            out.append((lexeme, tok))

    # 5) al final, cerrar todos los niveles de indent
    # 5) al final, cerrar todos los niveles de indent
    while len(indent_stack) > 1:
        indent_stack.pop()
        out.append(("", "DEDENT"))

    # 6) siempre se emite el DEDENT raíz que exige la suite
    out.append(("", "DEDENT"))
    return out
'''

    parts = [
        header,
        "# --- dfa_alternatives (autogenerado) --------------------------",
        f"dfa_alternatives = {json_alts}",
        "# --- runtime --------------------------------------------------",
        runtime,
        "# --- trailer --------------------------------------------------",
        trailer,
    ]
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(p for p in parts if p.strip()))

    print(f"✔ Lexer generado en «{out_file}»")

def main():
    print("=== Generando analizador léxico con YALex ===")
    try:
        res = integrate_yalex_pipeline("lexer.yal", use_minimization=True)
        generate_lexer_code(res)
        print("=== Listo. Ejecuta tus tests. ===")
    except Exception as exc:
        print("⚠ Error durante la generación:", exc, file=sys.stderr)

if __name__ == "__main__":
    main()
