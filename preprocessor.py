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
      - Literales escritos entre comillas simples,
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

        # Manejo de literales preformateados: Si se encuentra "LIT<" lo dejamos intacto.
        if expr.startswith("LIT<", i):
            j = expr.find(">", i + 4)
            if j == -1:
                raise ValueError("No se encontró '>' en LIT<…> a partir de la posición " + str(i))
            token = expr[i:j+1]
            i = j + 1
            print(f"DEBUG: parse_expr - encontrado LIT<…>: {token!r}")
            result.append(token)
            continue

        # Literales entre comillas simples
        if c == "'":
            j = expr.find("'", i+1)
            if j == -1:
                raise ValueError("No se encontró comilla de cierre en posición " + str(i))
            literal_content = expr[i+1:j]
            # Decodificar secuencias de escape (por ejemplo, "\\n" a "\n")
            literal_content = bytes(literal_content, "utf-8").decode("unicode_escape")
            token = f"LIT<<{literal_content}>>"
            print(f"DEBUG: parse_expr - literal entre comillas: {token!r}")
            i = j + 1
            if i < end and expr[i] in ('+', '?', '*'):
                op = expr[i]
                if op == '+':
                    token = f"({token}·{token}*)"
                elif op == '?':
                    token = f"({token}|ε)"
                elif op == '*':
                    token = token + "*"
                print(f"DEBUG: parse_expr - cuantificador '{op}' aplicado a literal: {token!r}")
                i += 1
            result.append(token)
            continue

        # Procesamiento de clases de caracteres [ ... ]
        if c == '[':
            j = expr.find(']', i+1)
            if j == -1:
                raise ValueError("No se encontró ']' para clase de caracteres iniciada en la posición " + str(i))
            else:
                content = expr[i+1:j]
                expanded = expand_charclass_cached(content)
                i = j+1
                if i < end and expr[i] in ('+', '?', '*'):
                    op = expr[i]
                    # Envolver la expansión completa en LIT<<…>>
                    literal = f"LIT<<{expanded}>>"
                    if op == '+':
                        literal = f"({literal}·{literal}*)"
                    elif op == '?':
                        literal = f"({literal}|ε)"
                    else:  # '*'
                        literal = literal + "*"
                    print(f"DEBUG: parse_expr - cuantificador '{op}' aplicado a clase: {literal!r}")
                    i += 1
                    result.append(literal)
                else:
                    result.append(f"LIT<<{expanded}>>")
                print(f"DEBUG: parse_expr - clase de caracteres [{content!r}] expandida a: {expanded!r}")
            continue

        # Secuencias con backslash
        if c == '\\':
            if i + 1 < end:
                result.append(decode_escape(expr[i+1]))
                i += 2
            else:
                result.append('\\')
                i += 1
            continue

        # Grupo con paréntesis
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

        # Llaves { ... } con cuantificadores
        if c == '{':
            j = expr.find('}', i+1)
            if j != -1 and (j - i) >= 2 and expr[j-1] in "+?*":
                qgroup_content = expr[i+1:j-1]
                qgroup_op = expr[j-1]
                token = f"{{{qgroup_content}}}{qgroup_op}"
                result.append(token)
                i = j+1
            else:
                result.append(c)
                i += 1
            continue

        # Caracter alfanumérico suelto
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

        # Operadores y otros caracteres
        if c in ('|', '·'):
            result.append(c)
            i += 1
            continue

        result.append(c)
        i += 1

    # Si se esperaba un cierre pero se llegó al final, lanzamos un error.
    if closing is not None:
        raise ValueError(f"No se encontró el carácter de cierre {closing} en la expresión")
    return "".join(result), i

def preprocess_expression_manual(expression):
    expr = expression.replace("\n", "\n")
    processed, pos = parse_expr(expr, 0, len(expr))
    if pos != len(expr):
        raise ValueError("No se consumió toda la expresión")
    # Si el resultado está compuesto únicamente por tokens LIT<<…>>,
    # se reensambla en un único literal. Si hay otros operadores o símbolos,
    # se deja intacto.
    if re.fullmatch(r"(LIT<<[^<>]*>>)+", processed):
        tokens = re.findall(r"LIT<<([^<>]*)>>", processed)
        processed = "LIT<<" + "".join(tokens) + ">>"
    return processed

def tokenize_postfix(postfix_str):
    """
    Tokeniza la notación postfix respetando los literales delimitados por LIT< ... >.
    Retorna una lista de objetos Symbol.
    """
    tokens = []
    i = 0
    n = len(postfix_str)
    while i < n:
        # Saltar espacios en blanco
        while i < n and postfix_str[i].isspace():
            i += 1
        if i >= n:
            break
        # Si el token comienza con LIT<, consumir todo el literal hasta el '>'
        if postfix_str.startswith("LIT<", i):
            start = i
            i += 4  # omitir "LIT<"
            literal_chars = []
            while i < n and postfix_str[i] != ">":
                literal_chars.append(postfix_str[i])
                i += 1
            if i >= n:
                raise ValueError("No se encontró '>' para token literal iniciado en la posición " + str(start))
            # Consumir el '>'
            i += 1
            literal_content = "".join(literal_chars)
            # Decodificar secuencias escapadas (por ejemplo, "\\t" → "\t")
            literal_converted = bytes(literal_content, "utf-8").decode("unicode_escape")
            tokens.append(Symbol(literal_converted, SymbolType.LITERAL))
        else:
            # Si no es literal, el token es un solo carácter (operador o literal)
            ch = postfix_str[i]
            if ch in {'*', '|', '·', '+', '?'}:
                tokens.append(Symbol(ch, SymbolType.OPERATOR))
            else:
                tokens.append(Symbol(ch, SymbolType.LITERAL))
            i += 1
    return tokens

if __name__ == "__main__":
    # Prueba con las reglas de comentarios
    test_expr_line = "'//' [^\\n]* '\\n'"
    test_expr_block = "'/*' ( _ )* '*/'"
    try:
        preprocessed_line = preprocess_expression_manual(test_expr_line)
        print("Expresión original (comentario línea):", test_expr_line)
        print("Preprocesada (comentario línea):", preprocessed_line)
    except Exception as e:
        print("Error procesando comentario línea:", e)
    try:
        preprocessed_block = preprocess_expression_manual(test_expr_block)
        print("Expresión original (comentario bloque):", test_expr_block)
        print("Preprocesada (comentario bloque):", preprocessed_block)
    except Exception as e:
        print("Error procesando comentario bloque:", e)
