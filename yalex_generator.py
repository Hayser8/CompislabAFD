import json

def clean_block(block):
    """
    Limpia un bloque de texto (por ejemplo, header o trailer) de la siguiente manera:
      1. Separa el bloque en líneas.
      2. Si la primera línea es exactamente "{" se elimina.
      3. Si la última línea es exactamente "}" se elimina.
      4. Une las líneas restantes.
      5. Cuenta las llaves de apertura y cierre en el contenido resultante; si faltan llaves de cierre,
         las agrega al final.
    """
    lines = block.splitlines()
    # Elimina la primera línea si es exactamente "{"
    if lines and lines[0].strip() == "{":
        lines = lines[1:]
    # Elimina la última línea si es exactamente "}"
    if lines and lines[-1].strip() == "}":
        lines = lines[:-1]
    cleaned = "\n".join(lines).rstrip()
    
    # Verifica el balance de llaves en el contenido interno
    open_braces = cleaned.count("{")
    close_braces = cleaned.count("}")
    if open_braces > close_braces:
        # Agrega las llaves de cierre faltantes
        cleaned += "\n" + "}" * (open_braces - close_braces)
    
    return cleaned


def generate_lexer_code(pipeline_result, output_filename="thelexer.py"):
    """
    Genera el código fuente del analizador léxico a partir del pipeline_result.
    Se incluye:
      - El header (limpio con clean_block).
      - La definición de la lista de alternativas para "gettoken" (usando su DFA minimizado).
      - Las funciones simulate_dfa, get_token y scan.
      - El trailer (limpio con clean_block).
    Se escribe el archivo final en secciones para evitar que las llaves internas del header/trailer
    interfieran con la interpolación de f-strings.
    """
    header = clean_block(pipeline_result["header"])
    trailer = clean_block(pipeline_result["trailer"])
    rules = pipeline_result["rules"]

    main_rule = "gettoken"
    if main_rule not in rules or len(rules[main_rule]) == 0:
        raise Exception("No se encontró la regla principal 'gettoken'")
    dfa_list = rules[main_rule]

    dfa_alternatives = []
    for entry in dfa_list:
        min_dfa = entry["min_dfa"]
        # Convertir los estados a cadena para asegurar la serialización JSON
        start_state = str(min_dfa.minimized_start)
        final_states = [str(s) for s in min_dfa.minimized_final]
        serializable_transitions = {}
        for state, trans in min_dfa.minimized_transitions.items():
            state_key = str(state)
            if state_key not in serializable_transitions:
                serializable_transitions[state_key] = {}
            for symbol, target in trans.items():
                serializable_transitions[state_key][symbol] = str(target)
        dfa_alternatives.append({
            "regex": entry["regex"],
            "action": entry["action"],
            "dfa_transitions": serializable_transitions,
            "dfa_start": start_state,
            "dfa_final": final_states
        })

    dfa_alternatives_json = json.dumps(dfa_alternatives, indent=4)

    # Definir el cuerpo del código para las funciones del analizador léxico
    lexer_functions = """
def simulate_dfa(dfa, input_string):
    \"\"\"
    Simula el DFA dado (representado por un diccionario con:
      - dfa_transitions: dict con claves de estado (str) y valores dict {symbol: target_state (str)}
      - dfa_start: estado inicial (str)
      - dfa_final: lista de estados finales (str)
    ) sobre la cadena input_string.
    Retorna (token, advance) si se reconoce un token, o (None, 0) en caso contrario.
    \"\"\"
    state = dfa["dfa_start"]
    token = ""
    pos = 0
    last_final_state = None
    last_final_pos = 0
    while pos < len(input_string):
        ch = input_string[pos]
        state_trans = dfa["dfa_transitions"].get(str(state), {})
        if ch in state_trans:
            state = state_trans[ch]
            token += ch
            pos += 1
            if state in dfa["dfa_final"]:
                last_final_state = state
                last_final_pos = pos
        else:
            break
    if last_final_state is not None:
        return token[:last_final_pos], last_final_pos
    return None, 0

def get_token(input_string):
    \"\"\"
    Recorre todas las alternativas de DFA y retorna el token (y su acción) que tenga el mayor avance.
    Si ninguna alternativa reconoce un token, retorna (None, None, 0).
    \"\"\"
    best_token = None
    best_action = None
    best_length = 0
    for dfa in dfa_alternatives:
        token, length = simulate_dfa(dfa, input_string)
        if token is not None and length > best_length:
            best_token = token
            best_action = dfa["action"]
            best_length = length
    return best_token, best_action, best_length

def scan(input_string):
    \"\"\"
    Función principal del analizador léxico. Recorre la cadena de entrada extrayendo tokens y sus acciones.
    Retorna una lista de tuplas (token, action).
    \"\"\"
    tokens = []
    pos = 0
    while pos < len(input_string):
        token, action, advance = get_token(input_string[pos:])
        if token is None or advance == 0:
            raise Exception("Error léxico en: " + input_string[pos:])
        tokens.append((token, action))
        pos += advance
    return tokens
"""

    # Construir el código final concatenando las secciones sin usar un gran f-string
    code = "\n".join([
        header,
        "\n# --- DFA generados por YALex Generator (alternativas para \"gettoken\") ---\n",
        "dfa_alternatives = " + dfa_alternatives_json,
        "\n" + lexer_functions,
        "\n# --- Fin de la generación del analizador léxico ---\n",
        trailer
    ])

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"El analizador léxico ha sido generado en {output_filename}")

if __name__ == "__main__":
    from yalex_pipeline import integrate_yalex_pipeline
    pipeline_result = integrate_yalex_pipeline("lexer.yal", use_minimization=True)
    generate_lexer_code(pipeline_result)
