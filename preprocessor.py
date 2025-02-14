import re

# --- Definiciones de funciones de reemplazo, igual que en tu versión original ---
def replace_escaped(match):
    escaped_char = match.group("escaped_char")
    if escaped_char in ("(", ")", "{", "}"):
        return "§" + escaped_char
    elif escaped_char in ("+", "?", "*", "|", ".", "^", "$"):
        return "§" + escaped_char
    elif escaped_char == "n":
        return "§n"
    elif escaped_char == "t":
        return "§t"
    else:
        return "§" + escaped_char

def expand_quantifier_group(match):
    # Simplemente devuelve el grupo en la forma {contenido} cuantificador
    # tal como lo tenías en tu versión
    return "{" + match.group("qgroup_content") + "}" + match.group("qgroup_op")

def expand_range(match):
    start, end = match.group("range_start"), match.group("range_end")
    expanded = "|".join(chr(c) for c in range(ord(start), ord(end) + 1))
    return f"({expanded})"

def expand_list(match):
    chars = "|".join(match.group("list_content"))
    return f"({chars})"

def replace_plus(match):
    token = match.group("plus_token")
    return "(" + token + "·" + token + "*)"

def replace_question(match):
    token = match.group("question_token")
    return "(" + token + "|ε)"

# --- Construcción del patrón compuesto ---
_COMPOSITE_PATTERN = re.compile(
    r"(?P<escaped>\\(?P<escaped_char>.))|"
    r"(?P<qgroup>\{(?P<qgroup_content>[^}]+)(?P<qgroup_op>[+?*])\})|"
    r"(?P<range>\[(?P<range_start>[a-zA-Z0-9])\-(?P<range_end>[a-zA-Z0-9])\])|"
    r"(?P<list>\[(?P<list_content>[a-zA-Z0-9]+)\])|"
    r"(?P<plus>(?<!§)(?P<plus_token>(?:\((?:[^()]+|\([^()]*\))*\)|\{(?:[^{}]+|\{[^{}]*\})*\}|[a-zA-Z0-9]))\+)|"
    r"(?P<question>(?<!§)(?P<question_token>(?:\((?:[^()]+|\([^()]*\))*\)|\{(?:[^{}]+|\{[^{}]*\})*\}|[a-zA-Z0-9]))\?)"
)

def preprocess_expression(expression):
    """
    Realiza el preprocesamiento de la expresión en una sola pasada utilizando
    un patrón compuesto que captura todos los casos.
    """
    # Paso 1: Reemplazar saltos de línea y espacios
    expression = expression.replace("\n", "§n").replace(" ", "")
    
    result = []
    last_end = 0
    # Iteramos sobre todas las coincidencias en una sola pasada
    for m in _COMPOSITE_PATTERN.finditer(expression):
        start, end = m.span()
        # Agregamos la parte de la cadena sin coincidencias
        result.append(expression[last_end:start])
        
        if m.group("escaped"):
            replacement = replace_escaped(m)
        elif m.group("qgroup"):
            replacement = expand_quantifier_group(m)
        elif m.group("range"):
            replacement = expand_range(m)
        elif m.group("list"):
            replacement = expand_list(m)
        elif m.group("plus"):
            replacement = replace_plus(m)
        elif m.group("question"):
            replacement = replace_question(m)
        else:
            replacement = m.group(0)  # por si acaso
        result.append(replacement)
        last_end = end
    # Agregar el resto de la cadena
    result.append(expression[last_end:])
    return "".join(result)