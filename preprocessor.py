import re

def expand_range(match):
    start, end = match.group(1), match.group(2)
    expanded = "|".join(chr(c) for c in range(ord(start), ord(end) + 1))
    return f"({expanded})"

def expand_list(match):
    # Une cada carácter con "|" para formar una alternancia.
    chars = "|".join(match.group(1))
    return f"({chars})"

def replace_escaped(match):
    """
    Procesa las secuencias escapadas:
      - Ahora, si se escapan paréntesis o llaves, se antepone el marcador § para que
        sean tratados como literales y no como símbolos de agrupación.
      - Si se escapan operadores (como +, ?, *, etc.), se antepone el marcador §.
      - Los escapes especiales \n y \t se convierten en "§n" y "§t".
      - Para cualquier otro carácter, se antepone §.
    """
    escaped_char = match.group(1)
    if escaped_char in ("(", ")", "{", "}"):
        # Se modificó para que estos caracteres se traten como literales.
        return "§" + escaped_char
    elif escaped_char in ("+", "?", "*", "|", ".", "^", "$"):
        return "§" + escaped_char
    elif escaped_char == "n":
        return "§n"
    elif escaped_char == "t":
        return "§t"
    else:
        return "§" + escaped_char

def preprocess_expression(expression):
    """
    Preprocesa la expresión haciendo lo siguiente:
      1. Reemplaza los saltos de línea reales por "§n".
      2. Elimina los espacios.
      3. Procesa las secuencias escapadas (añadiendo el marcador § según corresponda).
      4. Corrige agrupamientos con cuantificador dentro (por ejemplo, transforma "{[ei]+}" en "{[ei]}+").
      5. Expande clases de caracteres:
            - Rango: [0-3]  → (0|1|2|3)
            - Lista: [ae03] → (a|e|0|3)
      6. Transforma los operadores no escapados aplicados a un token:
            token+ → (token.token*)
            token? → (token|ε)
         (El lookbehind (?<!§) evita transformar aquellos precedidos por §).
    """
    # 1. Reemplaza saltos de línea reales por "§n"
    expression = expression.replace("\n", "§n")
    # 2. Elimina espacios
    expression = expression.replace(" ", "")
    # 3. Procesa las secuencias escapadas
    expression = re.sub(r"\\(.)", replace_escaped, expression)
    # 4. Corrige agrupamientos con cuantificador dentro de llaves
    expression = re.sub(r"\{([^}]+)([+?*])\}", r"{\1}\2", expression)
    # 5. Expande rangos y listas
    expression = re.sub(r"\[([a-zA-Z0-9])\-([a-zA-Z0-9])\]", expand_range, expression)
    expression = re.sub(r"\[([a-zA-Z0-9]+)\]", expand_list, expression)
    # 6. Transforma cuantificadores + y ? aplicados a un token no escapado,
    # permitiendo un nivel de agrupamiento anidado.
    expression = re.sub(
        r"(?<!§)((?:\((?:[^()]+|\([^()]*\))*\)|\{(?:[^{}]+|\{[^{}]*\})*\}|[a-zA-Z0-9]))\+",
        lambda m: "(" + m.group(1) + "." + m.group(1) + "*)",
        expression
    )
    expression = re.sub(
        r"(?<!§)((?:\((?:[^()]+|\([^()]*\))*\)|\{(?:[^{}]+|\{[^{}]*\})*\}|[a-zA-Z0-9]))\?",
        lambda m: "(" + m.group(1) + "|ε)",
        expression
    )
    return expression
