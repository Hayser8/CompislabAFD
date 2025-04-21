# yalex_generator.py ─ genera «lexeitor.py» a partir de lexer.yal
import json
import sys
from yalex_pipeline import integrate_yalex_pipeline


# ─────────────────────────── helpers ──────────────────────────────
def _clean_block(block: str) -> str:
    """Recorta llaves “{ … }” sobrantes de los bloques header/trailer."""
    lines = block.splitlines()
    if lines and lines[0].strip() == "{":
        lines = lines[1:]
    if lines and lines[-1].strip() == "}":
        lines = lines[:-1]
    body = "\n".join(lines).rstrip()
    diff = body.count("{") - body.count("}")
    return body + ("\n" + "}" * diff if diff > 0 else "")


# ──────────────────────── generador core ──────────────────────────
def generate_lexer_code(pipeline_result, out_file: str = "lexeitor.py"):
    header = _clean_block(pipeline_result["header"])
    trailer = _clean_block(pipeline_result["trailer"])
    rules = pipeline_result["rules"]

    if not rules.get("gettoken"):
        raise KeyError("Regla principal «gettoken» no encontrada")

    dfa_alts = []
    for ix, entry in enumerate(rules["gettoken"]):
        if not isinstance(entry, dict):
            raise TypeError(f"Entrada #{ix} no es dict")
        for req in ("min_dfa", "action"):
            if req not in entry:
                raise KeyError(f"Entrada #{ix} sin clave «{req}»")

        mdfa = entry["min_dfa"]
        start = str(mdfa.minimized_start)
        finals = {str(s) for s in mdfa.minimized_final}
        st_actions = {str(st): act
                      for st, act in getattr(mdfa, "state_actions", {}).items()}

        trans = {}
        for st, tbl in mdfa.minimized_transitions.items():
            k = str(st)
            for sym, tgt in tbl.items():
                # ε‑transición final               ↓↓↓
                if sym.startswith("0:__EOF_"):
                    finals.add(k)
                    if str(tgt) in st_actions and k not in st_actions:
                        st_actions[k] = st_actions[str(tgt)]
                    continue
                if sym == ":":          # clave de longitud 0 → se descarta
                    continue
                trans.setdefault(k, {})[sym] = str(tgt)

        dfa_alts.append({
            "regex": entry["regex"],
            "action": entry["action"],
            "alternatives": entry.get("alternatives", []),
            "dfa_transitions": trans,
            "dfa_start": start,
            "dfa_final": sorted(finals),
            "state_actions": st_actions,
        })

    json_alts = json.dumps(dfa_alts, indent=4)

    # ───────────── runtime que se incrusta en lexeitor.py ──────────
    runtime = r'''
import re, sys

# ——————————— 1. clase de error propio ————————————
class LexerError(Exception):
    """Errores detectados durante el análisis léxico."""
    def __init__(self, msg, line, col):
        super().__init__(f"[LÉXICO] L{line}:C{col}: {msg}")
        self.line, self.column = line, col


# ——————————— 2. utilidades DFA / decode ————————————
def decode_robust_key(key: str):
    """Convierte las claves codificadas del DFA en (es_conjunto, long, charset)."""
    if key.startswith("LIT<<") and key.endswith(">>"):
        lit = key[5:-2];  return False, len(lit), {lit}
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
    """Devuelve (lexema, long, estado_final) o (None,0,None) si no hay match."""
    state, best, pos = dfa["dfa_start"], ("", 0, None), 0
    while pos < len(text):
        chunk = text[pos:]
        matched = False
        for sym, tgt in dfa["dfa_transitions"].get(state, {}).items():
            is_set, ln, charset = decode_robust_key(sym)
            if ln > len(chunk):
                continue
            probe = chunk[:ln]
            if (probe in charset) if is_set else (probe == sym):
                state, pos, matched = tgt, pos + ln, True
                if state in dfa["dfa_final"]:
                    best = (text[:pos], pos, state)
                break
        if not matched:
            break
    return best if best[1] else (None, 0, None)


# ——————————— 3. tablas rápidas ————————————
_token_map = {
    "+": "PLUS",    "-": "MINUS",    "*": "TIMES",   "/": "DIV",   "%": "MODULO",
    "==": "EQUAL",  "!=": "NOT_EQUAL",
    "<": "LESS_THAN", "<=": "LESS_EQUAL",
    ">": "GREATER_THAN", ">=": "GREATER_EQUAL",
    "=": "ASSIGN",  ";": "SEMICOLON", ",": "COMMA",
    "(": "LPAREN",  ")": "RPAREN",   "{": "LBRACE",  "}": "RBRACE",
    "[": "LBRACKET", "]": "RBRACKET"
}
_num = re.compile(r"^[0-9]+$")
_flt = re.compile(r"^[0-9]+\.[0-9]+$")
_id  = re.compile(r"^[A-Za-z_][A-Za-z_0-9]*$")


def _categorize(lxm: str):
    if lxm in keywords:   return keywords[lxm]
    if lxm in _token_map: return _token_map[lxm]
    if _num.match(lxm):   return "INTEGER"
    if _flt.match(lxm):   return "FLOAT"
    if _id.match(lxm):    return "IDENTIFIER"
    if lxm.startswith("//"): return "COMMENT"
    if lxm.startswith("/*"): return "MULTILINE_COMMENT"
    if lxm.startswith('"'):  return "STRING"
    if lxm == "\n":          return "NEWLINE"
    if all(c in " \t\r" for c in lxm): return "WHITESPACE"
    return "UNKNOWN"


# ——————————— 4. estado global de posición ————————————
_cur_line, _cur_col = 1, 1   # columnas inician en 1


# ——————————— 5. get_token con detección de errores ————————————
def get_token(text: str):
    global _cur_line, _cur_col

    best_lx, best_ac, best_ln = None, None, 0

    # 1. probar DFA
    for dfa in dfa_alternatives:
        lx, ln, st = simulate_dfa(dfa, text)
        if ln > best_ln:
            best_ln, best_lx = ln, lx
            best_ac = dfa["state_actions"].get(str(st)) or dfa["action"]

    # 2. fallbacks + detección manual de errores
    two = text[:2]

    # comentario de bloque
    if text.startswith("/*"):
        end = text.find("*/", 2)
        if end != -1:
            return text[:end+2], "MULTILINE_COMMENT", end+2
        raise LexerError("Comentario de bloque sin cerrar", _cur_line, _cur_col)

    # string
    if text.startswith('"'):
        i, escaped = 1, False
        while i < len(text):
            if not escaped and text[i] == '"':
                return text[:i+1], "STRING", i+1
            escaped = (not escaped and text[i] == '\\\\')
            i += 1
        raise LexerError("Cadena de caracteres sin comillas de cierre",
                         _cur_line, _cur_col)

    # operadores de dos caracteres
    if two in _token_map and best_ln < 2:
        return two, _token_map[two], 2

    # tokens “simples” si DFA no ayudó
    if best_ln == 0 and text:
        ch = text[0]

        if ch in _token_map:
            return ch, _token_map[ch], 1

        if ch.isalpha() or ch == "_":
            j = 1
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            lx = text[:j]
            return lx, keywords.get(lx, "IDENTIFIER"), j

        if ch.isdigit():
            i = 0
            while i < len(text) and text[i].isdigit():
                i += 1
            if i < len(text) and text[i] == ".":
                j = i + 1
                while j < len(text) and text[j].isdigit():
                    j += 1
                if j > i + 1:
                    return text[:j], "FLOAT", j
            return text[:i], "INTEGER", i

    # 3. interpretar la acción si era “unified”
    if best_ac in (None, "unified", "ACCEPT") and best_lx is not None:
        best_ac = _categorize(best_lx)

    return best_lx, best_ac, best_ln


# ——————————— 6. scan con actualización línea/col ————————————
def scan(text: str):
    global _cur_line, _cur_col
    out, i = [], 0
    SKIP = {"WHITESPACE", "NEWLINE", "COMMENT", "MULTILINE_COMMENT"}

    while i < len(text):
        lx, ac, ln = get_token(text[i:])

        if ln == 0:
            raise LexerError("Símbolo desconocido", _cur_line, _cur_col)

        # actualizar contadores de posición
        segmento = text[i:i+ln]
        nl = segmento.count("\n")
        if nl:
            _cur_line += nl
            _cur_col = 1 + len(segmento) - segmento.rfind("\n")
        else:
            _cur_col += ln

        if ac not in SKIP:
            out.append((lx, ac))

        i += ln

    return out
'''

    # ensamblar archivo destino
    parts = [
        header,
        "# --- dfa_alternatives (autogenerado) --------------------------",
        f"dfa_alternatives = {json_alts}",
        "# --- runtime --------------------------------------------------",
        runtime,
        "# --- trailer --------------------------------------------------",
        trailer
    ]
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(p for p in parts if p.strip()))
    print(f"✔ Lexer generado en «{out_file}»")


# ────────────────────────── CLI simple ───────────────────────────
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
