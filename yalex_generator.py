import json
from yalex_pipeline import integrate_yalex_pipeline

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
    if lines and lines[0].strip() == "{":
        lines = lines[1:]
    if lines and lines[-1].strip() == "}":
        lines = lines[:-1]
    cleaned = "\n".join(lines).rstrip()
    open_braces = cleaned.count("{")
    close_braces = cleaned.count("}")
    if open_braces > close_braces:
        cleaned += "\n" + "}" * (open_braces - close_braces)
    return cleaned

def generate_lexer_code(pipeline_result, output_filename="lexeitor.py"):
    """
    Genera el código fuente del analizador léxico a partir del pipeline_result.
    Se incluye:
      - El header (limpio con clean_block).
      - La definición de la lista de alternativas para "gettoken" (usando su DFA minimizado).
      - Las funciones decode_robust_key, simulate_dfa, get_token y scan.
      - El trailer (limpio con clean_block).
    """
    header = clean_block(pipeline_result["header"])
    trailer = clean_block(pipeline_result["trailer"])
    rules = pipeline_result["rules"]

    main_rule = "gettoken"
    if main_rule not in rules or len(rules[main_rule]) == 0:
        raise Exception("No se encontró la regla principal 'gettoken'")
    dfa_list = rules[main_rule]

    # Construimos la lista de alternativas a partir del DFA minimizado unificado
    dfa_alternatives = []
    for entry in dfa_list:
        min_dfa = entry["min_dfa"]
        # Se obtienen los estados de inicio y finales (convertidos a string)
        start_state = str(min_dfa.minimized_start)
        final_states = [str(s) for s in min_dfa.minimized_final]
        serializable_transitions = {}
        # Serializamos las transiciones del DFA minimizado
        for state, trans in min_dfa.minimized_transitions.items():
            state_key = str(state)
            if state_key not in serializable_transitions:
                serializable_transitions[state_key] = {}
            for symbol, target in trans.items():
                serializable_transitions[state_key][symbol] = str(target)
        # Se añade además la lista de alternativas originales para poder descifrar la acción
        dfa_alternatives.append({
            "regex": entry["regex"],
            "action": entry["action"],  # se usa "unified" en el DFA unificado
            "alternatives": entry.get("alternatives", []),
            "dfa_transitions": serializable_transitions,
            "dfa_start": start_state,
            "dfa_final": final_states
        })

    dfa_alternatives_json = json.dumps(dfa_alternatives, indent=4)

    # Funciones del lexer que se incluirán en el archivo generado
    lexer_functions = (
        "def decode_robust_key(key):\n"
        "    \"\"\"\n"
        "    Decodifica manualmente una clave robusta.\n"
        "    Si la clave comienza con 'LIT<<' y termina con '>>', se remueven estos delimitadores.\n"
        "    Luego, si la clave comienza con dígitos seguidos de ':', se extrae la longitud y se divide el contenido\n"
        "    en alternativas usando '|' como separador. Si el contenido no termina en ')', se asume literal de longitud 1.\n"
        "    Retorna (True, longitud, set(alternativas)) si se cumple; de lo contrario, (False, None, None).\n"
        "    \"\"\"\n"
        "    if not isinstance(key, str):\n"
        "        key = str(key)\n"
        "    if key.startswith(\"LIT<<\") and key.endswith(\">>\"):\n"
        "        key = key[5:-2]\n"
        "\n"
        "    i = 0\n"
        "    while i < len(key) and key[i].isdigit():\n"
        "        i += 1\n"
        "    if i > 0 and i < len(key) and key[i] == ':':\n"
        "        if i+1 < len(key) and key[i+1] == '(' and key[-1] == ')':\n"
        "            length_val = 0\n"
        "            for j in range(i):\n"
        "                length_val = length_val * 10 + (ord(key[j]) - ord('0'))\n"
        "            alternatives_str = key[i+2:-1]\n"
        "            alt_list = alternatives_str.split('|')\n"
        "            return True, length_val, set(alt_list)\n"
        "        else:\n"
        "            return True, 1, set([key[i+1:]])\n"
        "    if key.startswith(\":\"):\n"
        "        content = key[1:]\n"
        "        if content.startswith(\"(\") and content.endswith(\")\"):\n"
        "            content = content[1:-1]\n"
        "        if '|' in content:\n"
        "            alt_list = content.split(\"|\")\n"
        "            return True, 1, set(alt_list)\n"
        "        else:\n"
        "            return True, 1, set([content])\n"
        "    return False, None, None\n\n"
        "def simulate_dfa(dfa, input_string):\n"
        "    state = dfa['dfa_start']\n"
        "    token = ''\n"
        "    pos = 0\n"
        "    last_final_state = None\n"
        "    last_final_pos = 0\n\n"
        "    while pos < len(input_string):\n"
        "        ch_real = input_string[pos]\n"
        "        ch = ch_real\n\n"
        "        state_trans = dfa['dfa_transitions'].get(str(state), {})\n"
        "        found_transition = None\n"
        "        for key, target in state_trans.items():\n"
        "            robust, length_val, alt_set = decode_robust_key(key)\n"
        "            if robust:\n"
        "                if ch in alt_set:\n"
        "                    found_transition = target\n"
        "                    break\n"
        "            else:\n"
        "                if ch == key:\n"
        "                    found_transition = target\n"
        "                    break\n"
        "        if found_transition is not None:\n"
        "            state = found_transition\n"
        "            token += ch_real\n"
        "            pos += 1\n"
        "            if state in dfa['dfa_final']:\n"
        "                last_final_state = state\n"
        "                last_final_pos = pos\n"
        "        else:\n"
        "            break\n\n"
        "    if last_final_state is not None:\n"
        "        return token, last_final_pos\n"
        "    else:\n"
        "        return None, 0\n\n"
        "def get_token(input_string):\n"
        "    \"\"\"\n"
        "    Recorre todas las alternativas de DFA y retorna el token (y su acción) que tenga el mayor avance.\n"
        "    Si ninguna alternativa reconoce un token, retorna (None, None, 0).\n"
        "    Antes de simular el DFA se verifica manualmente si la entrada comienza con un comentario.\n"
        "    \"\"\"\n"
        "    # Verificar comentarios de bloque manualmente:\n"
        "    if input_string.startswith(\"/*\"):\n"
        "        end_idx = input_string.find(\"*/\")\n"
        "        if end_idx == -1:\n"
        "            raise Exception(\"Comentario de bloque sin cerrar\")\n"
        "        token = input_string[:end_idx+2]  # incluir \"*/\"\n"
        "        return token, \"MULTILINE_COMMENT\", len(token)\n"
        "    # Verificar comentarios de línea manualmente:\n"
        "    if input_string.startswith(\"//\"):\n"
        "        end_idx = input_string.find(\"\\n\")\n"
        "        if end_idx == -1:\n"
        "            end_idx = len(input_string)\n"
        "        token = input_string[:end_idx+1]  # incluir el salto de línea\n"
        "        return token, \"COMMENT\", len(token)\n"
        "\n"
        "    best_token = None\n"
        "    best_action = None\n"
        "    best_length = 0\n"
        "    for dfa in dfa_alternatives:\n"
        "        token, length = simulate_dfa(dfa, input_string)\n"
        "        if token is not None and length > best_length:\n"
        "            best_token = token\n"
        "            best_action = dfa['action']\n"
        "            best_length = length\n"
        "\n"
        "    if best_token is None or best_length == 0:\n"
        "        return None, None, 0\n"
        "\n"
        "    if best_action == \"unified\":\n"
        "        if best_token.startswith('\"') and best_token.endswith('\"'):\n"
        "            best_action = \"STRING\"\n"
        "        elif best_token.isspace():\n"
        "            best_action = \"NEWLINE\" if \"\\n\" in best_token else \"WHITESPACE\"\n"
        "        elif best_token in keywords:\n"
        "            best_action = keywords[best_token]\n"
        "        elif best_token and (best_token[0].isalpha() or best_token[0] == '_'):\n"
        "            best_action = \"IDENTIFIER\"\n"
        "        elif best_token.isdigit():\n"
        "            best_action = \"INTEGER\"\n"
        "        elif best_token.count('.') == 1 and best_token.replace('.', '').isdigit():\n"
        "            best_action = \"FLOAT\"\n"
        "        else:\n"
        "            mapping = {\n"
        "                '+': \"PLUS\",\n"
        "                '-': \"MINUS\",\n"
        "                '*': \"TIMES\",\n"
        "                '/': \"DIV\",\n"
        "                '%': \"MODULO\",\n"
        "                '==': \"EQUAL\",\n"
        "                '!=': \"NOT_EQUAL\",\n"
        "                '<': \"LESS_THAN\",\n"
        "                '<=': \"LESS_EQUAL\",\n"
        "                '>': \"GREATER_THAN\",\n"
        "                '>=': \"GREATER_EQUAL\",\n"
        "                '=': \"ASSIGN\",\n"
        "                ';': \"SEMICOLON\",\n"
        "                ',': \"COMMA\",\n"
        "                '(': \"LPAREN\",\n"
        "                ')': \"RPAREN\",\n"
        "                '{': \"LBRACE\",\n"
        "                '}': \"RBRACE\",\n"
        "                '[': \"LBRACKET\",\n"
        "                ']': \"RBRACKET\"\n"
        "            }\n"
        "            best_action = mapping.get(best_token, \"UNKNOWN\")\n"
        "\n"
        "    return best_token, best_action, best_length\n\n"
        "def scan(input_string):\n"
        "    tokens = []\n"
        "    pos = 0\n"
        "    while pos < len(input_string):\n"
        "        token, action, advance = get_token(input_string[pos:])\n"
        "        if token is None or advance == 0:\n"
        "            raise Exception('Error léxico en: ' + input_string[pos:])\n"
        "        if action not in ('WHITESPACE', 'NEWLINE'):\n"
        "            tokens.append((token, action))\n"
        "        pos += advance\n"
        "    return tokens\n"
    )
    
    code_parts = [
        header,
        "# --- DFA generados por YALex Generator (alternativas para \"gettoken\") ---",
        f"dfa_alternatives = {dfa_alternatives_json}",
        lexer_functions,
        "# --- Fin de la generación del analizador léxico ---",
        trailer
    ]
    
    final_code = "\n\n".join(part for part in code_parts if part.strip())
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(final_code)
    
    print(f"El analizador léxico ha sido generado en {output_filename}")

def main():
    """
    Ejecuta la generación del lexer a partir de 'lexer.yal'.
    """
    print("=== Iniciando generación de analizador léxico con YALex ===")
    try:
        pipeline_result = integrate_yalex_pipeline("lexer.yal", use_minimization=True)
        generate_lexer_code(pipeline_result, output_filename="lexeitor.py")
        print("=== Generación completada. Archivo 'lexeitor.py' creado. ===")
    except Exception as e:
        print("Ocurrió un error durante la generación del lexer:", e)

if __name__ == "__main__":
    main()
