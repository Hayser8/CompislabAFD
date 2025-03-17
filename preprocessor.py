import re
from functools import lru_cache

@lru_cache(maxsize=None)
def expand_charclass_cached(content):
    """
    Expande una clase de caracteres dada su cadena de contenido.
    Elimina los caracteres '|' y comillas simples, detecta rangos (por ejemplo, a-z)
    y devuelve una expresión de alternancia.
    """
    content_clean = content.replace("|", "").replace("'", "")
    chars = []
    i = 0
    length = len(content_clean)
    while i < length:
        if i + 2 < length and content_clean[i+1] == '-':
            start, end = content_clean[i], content_clean[i+2]
            chars.extend(chr(c) for c in range(ord(start), ord(end) + 1))
            i += 3
        else:
            chars.append(content_clean[i])
            i += 1
    unique_chars = sorted(set(chars))
    return "(" + "|".join(unique_chars) + ")"

def parse_expr(expr, i, end, closing=None):
    """
    Procesa recursivamente la expresión desde la posición i hasta end.
    Si se indica un carácter de cierre (closing), se detiene cuando se lo encuentra.
    Retorna la cadena procesada y la nueva posición.
    """
    result = []
    while i < end:
        if closing is not None and expr[i] == closing:
            return "".join(result), i+1

        c = expr[i]
        if c == '\\':
            # Secuencia de escape: se reemplaza '\' por '§'
            if i+1 < end:
                result.append("§" + expr[i+1])
                i += 2
            else:
                result.append("§")
                i += 1
        elif c == '[':
            # Procesa una clase de caracteres: busca el cierre ']'
            j = expr.find(']', i+1)
            if j == -1:
                result.append(c)
                i += 1
            else:
                content = expr[i+1:j]
                expanded = expand_charclass_cached(content)
                result.append(expanded)
                i = j+1
                # Aplica operador si le sigue
                if i < end and expr[i] in ('+', '?', '*'):
                    op = expr[i]
                    if op == '+':
                        token = "(" + expanded + "·" + expanded + "*)"
                    elif op == '?':
                        token = "(" + expanded + "|ε)"
                    else:  # '*'
                        token = expanded + "*"
                    result[-1] = token
                    i += 1
        elif c == '(':
            # Procesa un grupo anidado recursivamente
            inner, new_i = parse_expr(expr, i+1, end, closing=')')
            token = "(" + inner + ")"
            i = new_i
            # Aplica operador si le sigue al grupo
            if i < end and expr[i] in ('+', '?', '*'):
                op = expr[i]
                if op == '+':
                    token = "(" + token + "·" + token + "*)"
                elif op == '?':
                    token = "(" + token + "|ε)"
                else:  # '*'
                    token = token + "*"
                i += 1
            result.append(token)
        elif c == '{':
            # Detecta grupo cuantificador del tipo {contenido operator}
            j = expr.find('}', i+1)
            if j != -1 and (j - i) >= 2 and expr[j-1] in "+?*":
                qgroup_content = expr[i+1:j-1]
                qgroup_op = expr[j-1]
                token = "{" + qgroup_content + "}" + qgroup_op
                result.append(token)
                i = j+1
            else:
                result.append(c)
                i += 1
        elif c.isalnum():
            # Token simple (alfanumérico)
            token = c
            i += 1
            # Aplica operador '+' o '?' o '*' si le sigue
            if i < end and expr[i] in ('+', '?', '*'):
                op = expr[i]
                if op == '+':
                    token = "(" + token + "·" + token + "*)"
                elif op == '?':
                    token = "(" + token + "|ε)"
                else:  # '*'
                    token = token + "*"
                i += 1
            result.append(token)
        elif c in ('|', '·'):
            # Operadores literales se copian
            result.append(c)
            i += 1
        else:
            # Otros caracteres se copian directamente
            result.append(c)
            i += 1
    return "".join(result), i

def preprocess_expression_manual(expression):
    """
    Preprocesa la expresión:
      - Reemplaza saltos de línea por "§n" y elimina espacios.
      - Procesa de forma recursiva secuencias de escape, clases de caracteres,
        grupos anidados y operadores '+' y '?' (y '*' sin transformación).
    """
    expr = expression.replace("\n", "§n").replace(" ", "")
    processed, _ = parse_expr(expr, 0, len(expr), closing=None)
    return processed

# --- Código de prueba del parser manual recursivo ---
if __name__ == "__main__":
    test_expr = "['a'-'z' 'A'-'Z' '_']"
    preprocessed_manual = preprocess_expression_manual(test_expr)
    print("Expresión original:", test_expr)
    print("Preprocesada (manual):", preprocessed_manual)

    test_expr2 = "['a'-'z' 'A'-'Z' '_'] (['a'-'z' 'A'-'Z' '_'] | ['0'-'9'])*"
    preprocessed_manual2 = preprocess_expression_manual(test_expr2)
    print("\nExpresión original:", test_expr2)
    print("Preprocesada (manual):", preprocessed_manual2)
