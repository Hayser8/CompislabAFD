from functools import lru_cache
from symbol import Symbol, SymbolType
import re

# Definimos un alfabeto completo usando caracteres reales.
# Se incluyen los caracteres ASCII imprimibles y los especiales de escape.
FULL_ALPHABET = [chr(i) for i in range(32, 127)] + ["\n", "\t", "\r"]

def decode_escape(seq):
    """Convierte una secuencia de escape en su carácter real."""
    mapping = {"n": "\n", "t": "\t", "r": "\r"}
    return mapping.get(seq, seq)

@lru_cache(maxsize=None)
def expand_charclass_cached(content):
    """
    Expande una clase de caracteres dada su cadena 'content'.
      - Si está negada (empieza con '^'), se calcula el complemento respecto a FULL_ALPHABET.
      - Combina rangos (por ejemplo, a-z).
      - Convierte secuencias con backslash a sus caracteres reales.
      - Devuelve una alternancia en forma de cadena, por ejemplo: "(a|b|...)".
    """
    print(f"DEBUG: expand_charclass_cached - contenido original: {content!r}")
    is_negated = False
    if content.startswith('^'):
        is_negated = True
        content = content[1:]
    content_clean = content.replace("|", "").replace("'", "")
    chars = []
    i = 0
    length = len(content_clean)
    while i < length:
        if i + 1 < length and content_clean[i] == '\\':
            next_char = content_clean[i+1]
            chars.append(decode_escape(next_char))
            i += 2
        elif i + 2 < length and content_clean[i+1] == '-':
            start, end = content_clean[i], content_clean[i+2]
            for c in range(ord(start), ord(end) + 1):
                chars.append(chr(c))
            i += 3
        else:
            ch = content_clean[i]
            chars.append(ch)
            i += 1
    if is_negated:
        full_set = set(FULL_ALPHABET)
        allowed = sorted(full_set - set(chars))
        result = "(" + "|".join(allowed) + ")"
        print(f"DEBUG: expand_charclass_cached - negado, resultado: {result!r}")
        return result
    else:
        unique_chars = sorted(set(chars))
        result = "(" + "|".join(unique_chars) + ")"
        print(f"DEBUG: expand_charclass_cached - resultado: {result!r}")
        return result

def parse_expr(expr, i, end, closing=None):
    """
    Procesa la expresión desde la posición i hasta end.
    Maneja:
      - Literales escritos entre comillas simples o dobles,
      - Clases de caracteres [ ... ] (se envuelven en LIT<…>),
      - Grupos (paréntesis) y cuantificadores (+, ?, *),
      - Secuencias con backslash.
    """
    result = []
    while i < end:
        if closing is not None and expr[i] == closing:
            return "".join(result), i + 1

        c = expr[i]
        if c.isspace():
            i += 1
            continue

        # Literales preformateados: "LIT<...>"
        if expr.startswith("LIT<", i):
            j = expr.find(">", i + 4)
            if j == -1:
                raise ValueError(f"No se encontró '>' en LIT<…> desde la posición {i}")
            token = expr[i:j+1]
            print(f"DEBUG: parse_expr - encontrado LIT<…>: {token!r}")
            result.append(token)
            i = j + 1
            continue

        # Literales entre comillas simples o dobles
        if c in ("'", '"'):
            quote = c
            j = i + 1
            literal_chars = []
            while j < end:
                if expr[j] == "\\" and j+1 < end:
                    literal_chars.append(expr[j:j+2])
                    j += 2
                elif expr[j] == quote:
                    break
                else:
                    literal_chars.append(expr[j])
                    j += 1
            if j >= end or expr[j] != quote:
                raise ValueError(f"No se encontró comilla de cierre para literal iniciado en posición {i}")
            raw = "".join(literal_chars)
            decoded = bytes(raw, "utf-8").decode("unicode_escape")
            token = f"LIT<<{decoded}>>"
            print(f"DEBUG: parse_expr - literal entre comillas ({quote}…{quote}): {token!r}")
            i = j + 1
            if i < end and expr[i] in ('+', '?', '*'):
                op = expr[i]
                if op == '+':
                    token = f"({token}·{token}*)"
                elif op == '?':
                    token = f"({token}|ε)"
                else:  # '*'
                    token = token + "*"
                print(f"DEBUG: parse_expr - cuantificador '{op}' aplicado a literal: {token!r}")
                i += 1
            result.append(token)
            continue

        # Clases de caracteres [ ... ]
        if c == '[':
            j = expr.find(']', i+1)
            if j == -1:
                raise ValueError(f"No se encontró ']' para clase iniciada en posición {i}")
            content = expr[i+1:j]
            expanded = expand_charclass_cached(content)
            i = j + 1
            if i < end and expr[i] in ('+', '?', '*'):
                op = expr[i]
                literal = f"LIT<<{expanded}>>"
                if op == '+':
                    literal = f"({literal}·{literal}*)"
                elif op == '?':
                    literal = f"({literal}|ε)"
                else:
                    literal = literal + "*"
                print(f"DEBUG: parse_expr - cuantificador '{op}' aplicado a clase: {literal!r}")
                i += 1
                result.append(literal)
            else:
                result.append(f"LIT<<{expanded}>>")
            print(f"DEBUG: parse_expr - clase [{content!r}] → {expanded!r}")
            continue

        # Secuencias escapadas
        if c == '\\':
            if i + 1 < end:
                result.append(decode_escape(expr[i+1]))
                i += 2
            else:
                result.append('\\')
                i += 1
            continue

        # Grupos (...)
        if c == '(':
            sub, new_i = parse_expr(expr, i+1, end, closing=')')
            token = f"({sub})"
            i = new_i
            if i < end and expr[i] in ('+', '?', '*'):
                op = expr[i]
                if op == '+':
                    token = f"({token}·{token}*)"
                elif op == '?':
                    token = f"({token}|ε)"
                else:
                    token = token + "*"
                print(f"DEBUG: parse_expr - cuantificador '{op}' aplicado a grupo: {token!r}")
                i += 1
            result.append(token)
            continue

        # Cuantificadores {m,n}
        if c == '{':
            j = expr.find('}', i+1)
            if j != -1 and (j - i) >= 2 and expr[j-1] in "+?*":
                content = expr[i+1:j-1]
                op = expr[j-1]
                token = f"{{{content}}}{op}"
                result.append(token)
                i = j + 1
            else:
                result.append(c)
                i += 1
            continue

        # Literales alfanuméricos sueltos
        if c.isalnum():
            token = c
            i += 1
            if i < end and expr[i] in ('+', '?', '*'):
                op = expr[i]
                if op == '+':
                    token = f"({token}·{token}*)"
                elif op == '?':
                    token = f"({token}|ε)"
                else:
                    token = token + "*"
                print(f"DEBUG: parse_expr - cuantificador '{op}' aplicado a literal alfanumérico: {token!r}")
                i += 1
            result.append(token)
            continue

        # Operadores y punto medio de concatenación
        if c in ('|', '·'):
            result.append(c)
            i += 1
            continue

        # Cualquier otro carácter
        result.append(c)
        i += 1

    # Si esperaba un cierre y no llegó
    if closing is not None:
        raise ValueError(f"No se encontró el carácter de cierre {closing}")
    return "".join(result), i

def preprocess_expression_manual(expression):
    expr = expression
    processed, pos = parse_expr(expr, 0, len(expr))
    if pos != len(expr):
        raise ValueError("No se consumió toda la expresión")
    # Reensamble si sólo hay literales
    if re.fullmatch(r"(LIT<<[^<>]*>>)+", processed):
        tokens = re.findall(r"LIT<<([^<>]*)>>", processed)
        processed = "LIT<<" + "".join(tokens) + ">>"
    return processed

def tokenize_postfix(postfix_str):
    """
    Tokeniza la notación postfix respetando los literales delimitados por LIT< ... >>.
    Retorna una lista de objetos Symbol.
    """
    tokens = []
    i = 0
    n = len(postfix_str)
    while i < n:
        while i < n and postfix_str[i].isspace():
            i += 1
        if i >= n:
            break
        if postfix_str.startswith("LIT<<", i):
            start = i
            i += 5
            literal_chars = []
            while i < n and not postfix_str.startswith(">>", i):
                literal_chars.append(postfix_str[i])
                i += 1
            if i >= n:
                raise ValueError(f"No se encontró '>>' para literal iniciado en {start}")
            i += 2
            content = "".join(literal_chars)
            decoded = bytes(content, "utf-8").decode("unicode_escape")
            tokens.append(Symbol(decoded, SymbolType.LITERAL))
        else:
            ch = postfix_str[i]
            if ch in {'*', '|', '·', '+', '?'}:
                tokens.append(Symbol(ch, SymbolType.OPERATOR))
            else:
                tokens.append(Symbol(ch, SymbolType.LITERAL))
            i += 1
    return tokens

if __name__ == "__main__":
    # Pruebas rápidas
    for test in ["'//'\n", "'/*' ( _ )* '*/'"]:
        try:
            out = preprocess_expression_manual(test)
            print(f"{test!r} → {out!r}")
        except Exception as e:
            print(f"Error en {test!r}: {e}")
