# Encabezado: Código Python que se copia en la salida
import sys
# Tabla de palabras clave reservadas
keywords = {
"if": "IF",
"else": "ELSE",
"while": "WHILE",
"return": "RETURN",
"int": "INT",
"float": "FLOAT",
"void": "VOID"
}

# --- DFA generados por YALex Generator (alternativas para "gettoken") ---

dfa_alternatives = [
    {
        "regex": "(whitespace+)(?=#$return \"WHITESPACE\"$#)|(newline)(?=#$return \"NEWLINE\"$#)|(number)(?=#$return \"INTEGER\"$#)|(floatnum)(?=#$return \"FLOAT\"$#)|(identifier)(?=#$if lxm in keywords: return keywords[lxm] return \"IDENTIFIER\"$#)|(('/*' ([^*] | '*' [^/])* '*' '/'))(?=#$return \"MULTILINE_COMMENT\"$#)|('//' [^\\n]* '\\n')(?=#$return \"COMMENT\"$#)|('\"' ([^\"\\n] | '\\\\' .)* '\"')(?=#$return \"STRING\"$#)|('+')(?=#$return \"PLUS\"$#)|('-')(?=#$return \"MINUS\"$#)|('*')(?=#$return \"TIMES\"$#)|('/')(?=#$return \"DIV\"$#)|('%')(?=#$return \"MODULO\"$#)|('==')(?=#$return \"EQUAL\"$#)|('!=')(?=#$return \"NOT_EQUAL\"$#)|('<')(?=#$return \"LESS_THAN\"$#)|('<=')(?=#$return \"LESS_EQUAL\"$#)|('>=')(?=#$return \"GREATER_EQUAL\"$#)|('>')(?=#$return \"GREATER_THAN\"$#)|('=')(?=#$return \"ASSIGN\"$#)|(';')(?=#$return \"SEMICOLON\"$#)|(',')(?=#$return \"COMMA\"$#)|('(')(?=#$return \"LPAREN\"$#)|(')')(?=#$return \"RPAREN\"$#)|('{')(?=#$return \"LBRACE\"$#)|('}')(?=#$return \"RBRACE\"$#)|('[')(?=#$return \"LBRACKET\"$#)|(']')(?=#$return \"RBRACKET\"$#)|(eof)(?=#$raise(\"Fin de archivo\")$#)",
        "action": "unified",
        "alternatives": [
            [
                "whitespace+",
                "return \"WHITESPACE\""
            ],
            [
                "newline",
                "return \"NEWLINE\""
            ],
            [
                "number",
                "return \"INTEGER\""
            ],
            [
                "floatnum",
                "return \"FLOAT\""
            ],
            [
                "identifier",
                "if lxm in keywords: return keywords[lxm] return \"IDENTIFIER\""
            ],
            [
                "('/*' ([^*] | '*' [^/])* '*' '/')",
                "return \"MULTILINE_COMMENT\""
            ],
            [
                "'//' [^\\n]* '\\n'",
                "return \"COMMENT\""
            ],
            [
                "'\"' ([^\"\\n] | '\\\\' .)* '\"'",
                "return \"STRING\""
            ],
            [
                "'+'",
                "return \"PLUS\""
            ],
            [
                "'-'",
                "return \"MINUS\""
            ],
            [
                "'*'",
                "return \"TIMES\""
            ],
            [
                "'/'",
                "return \"DIV\""
            ],
            [
                "'%'",
                "return \"MODULO\""
            ],
            [
                "'=='",
                "return \"EQUAL\""
            ],
            [
                "'!='",
                "return \"NOT_EQUAL\""
            ],
            [
                "'<'",
                "return \"LESS_THAN\""
            ],
            [
                "'<='",
                "return \"LESS_EQUAL\""
            ],
            [
                "'>='",
                "return \"GREATER_EQUAL\""
            ],
            [
                "'>'",
                "return \"GREATER_THAN\""
            ],
            [
                "'='",
                "return \"ASSIGN\""
            ],
            [
                "';'",
                "return \"SEMICOLON\""
            ],
            [
                "','",
                "return \"COMMA\""
            ],
            [
                "'('",
                "return \"LPAREN\""
            ],
            [
                "')'",
                "return \"RPAREN\""
            ],
            [
                "'{'",
                "return \"LBRACE\""
            ],
            [
                "'}'",
                "return \"RBRACE\""
            ],
            [
                "'['",
                "return \"LBRACKET\""
            ],
            [
                "']'",
                "return \"RBRACKET\""
            ],
            [
                "eof",
                "raise(\"Fin de archivo\")"
            ]
        ],
        "dfa_transitions": {
            "frozenset({frozenset({8, 52, 5, 7})})": {
                ":.": "frozenset({frozenset({9})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({8, 52, 5, 7})})"
            },
            "frozenset({frozenset({12, 13, 52})})": {
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({12, 13, 52})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({12, 13, 52})})"
            },
            "frozenset({frozenset({10, 52})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({10, 52})})"
            },
            "frozenset({frozenset({2, 52})})": {
                ":(\t|\r| )": "frozenset({frozenset({2, 52})})"
            },
            "frozenset({frozenset({52})})": {},
            "frozenset({frozenset({1, 3, 4, 6, 11, 14, 20, 23, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49})})": {
                ":(\t|\r| )": "frozenset({frozenset({2, 52})})",
                ":\n": "frozenset({frozenset({52})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({8, 52, 5, 7})})",
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({12, 13, 52})})",
                ":/*": "frozenset({frozenset({16, 18, 15})})",
                "://": "frozenset({frozenset({21, 22})})",
                ":\"": "frozenset({frozenset({24, 25, 27})})",
                ":+": "frozenset({frozenset({52})})",
                ":-": "frozenset({frozenset({52})})",
                ":*": "frozenset({frozenset({52})})",
                ":/": "frozenset({frozenset({52})})",
                ":%": "frozenset({frozenset({52})})",
                ":==": "frozenset({frozenset({52})})",
                ":!=": "frozenset({frozenset({52})})",
                ":<": "frozenset({frozenset({52})})",
                ":<=": "frozenset({frozenset({52})})",
                ":>=": "frozenset({frozenset({52})})",
                ":": "frozenset({frozenset({39})})",
                ":=": "frozenset({frozenset({52})})",
                ":;": "frozenset({frozenset({52})})",
                ":,": "frozenset({frozenset({52})})",
                ":(": "frozenset({frozenset({52})})",
                ":)": "frozenset({frozenset({52})})",
                ":{": "frozenset({frozenset({52})})",
                ":}": "frozenset({frozenset({52})})",
                ":[": "frozenset({frozenset({52})})",
                ":]": "frozenset({frozenset({52})})",
                "e": "frozenset({frozenset({50})})"
            },
            "frozenset({frozenset({16, 18, 15})})": {
                ":*": "frozenset({frozenset({17, 19})})",
                "99:(\t|\n|\r| |!|\"|#|$|%|&|'|(|)|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({16, 18, 15})})"
            },
            "frozenset({frozenset({17, 19})})": {
                "99:(\t|\n|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({16, 18, 15})})",
                ":/": "frozenset({frozenset({52})})"
            },
            "frozenset({frozenset({50})})": {
                "o": "frozenset({frozenset({51})})"
            },
            "frozenset({frozenset({26})})": {
                ".": "frozenset({frozenset({24, 25, 27})})"
            },
            "frozenset({frozenset({21, 22})})": {
                "98:(\t|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({21, 22})})",
                ":\n": "frozenset({frozenset({52})})"
            },
            "frozenset({frozenset({24, 25, 27})})": {
                "96:(\t|\r| |!|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({24, 25, 27})})",
                ":\\": "frozenset({frozenset({26})})",
                ":\"": "frozenset({frozenset({52})})"
            },
            "frozenset({frozenset({39})})": {
                ">": "frozenset({frozenset({52})})"
            },
            "frozenset({frozenset({9})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({10, 52})})"
            },
            "frozenset({frozenset({51})})": {
                "f": "frozenset({frozenset({52})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1, 3, 4, 6, 11, 14, 20, 23, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49})})",
        "dfa_final": [
            "frozenset({frozenset({8, 52, 5, 7})})",
            "frozenset({frozenset({12, 13, 52})})",
            "frozenset({frozenset({2, 52})})",
            "frozenset({frozenset({52})})",
            "frozenset({frozenset({10, 52})})"
        ]
    }
]

def decode_robust_key(key):
    """
    Decodifica manualmente una clave robusta.
    Si la clave comienza con 'LIT<<' y termina con '>>', se remueven estos delimitadores.
    Luego, si la clave comienza con dígitos seguidos de ':', se extrae la longitud y se divide el contenido
    en alternativas usando '|' como separador. Si el contenido no termina en ')', se asume literal de longitud 1.
    Retorna (True, longitud, set(alternativas)) si se cumple; de lo contrario, (False, None, None).
    """
    if not isinstance(key, str):
        key = str(key)
    if key.startswith("LIT<<") and key.endswith(">>"):
        key = key[5:-2]

    i = 0
    while i < len(key) and key[i].isdigit():
        i += 1
    if i > 0 and i < len(key) and key[i] == ':':
        if i+1 < len(key) and key[i+1] == '(' and key[-1] == ')':
            length_val = 0
            for j in range(i):
                length_val = length_val * 10 + (ord(key[j]) - ord('0'))
            alternatives_str = key[i+2:-1]
            alt_list = alternatives_str.split('|')
            return True, length_val, set(alt_list)
        else:
            return True, 1, set([key[i+1:]])
    if key.startswith(":"):
        content = key[1:]
        if content.startswith("(") and content.endswith(")"):
            content = content[1:-1]
        if '|' in content:
            alt_list = content.split("|")
            return True, 1, set(alt_list)
        else:
            return True, 1, set([content])
    return False, None, None

def simulate_dfa(dfa, input_string):
    state = dfa['dfa_start']
    token = ''
    pos = 0
    last_final_state = None
    last_final_pos = 0

    while pos < len(input_string):
        ch_real = input_string[pos]
        ch = ch_real

        state_trans = dfa['dfa_transitions'].get(str(state), {})
        found_transition = None
        for key, target in state_trans.items():
            robust, length_val, alt_set = decode_robust_key(key)
            if robust:
                if ch in alt_set:
                    found_transition = target
                    break
            else:
                if ch == key:
                    found_transition = target
                    break
        if found_transition is not None:
            state = found_transition
            token += ch_real
            pos += 1
            if state in dfa['dfa_final']:
                last_final_state = state
                last_final_pos = pos
        else:
            break

    if last_final_state is not None:
        return token, last_final_pos
    else:
        return None, 0

def get_token(input_string):
    """
    Recorre todas las alternativas de DFA y retorna el token (y su acción) que tenga el mayor avance.
    Si ninguna alternativa reconoce un token, retorna (None, None, 0).
    Antes de simular el DFA se verifica manualmente si la entrada comienza con un comentario.
    """
    # Verificar comentarios de bloque manualmente:
    if input_string.startswith("/*"):
        end_idx = input_string.find("*/")
        if end_idx == -1:
            raise Exception("Comentario de bloque sin cerrar")
        token = input_string[:end_idx+2]  # incluir "*/"
        return token, "MULTILINE_COMMENT", len(token)
    # Verificar comentarios de línea manualmente:
    if input_string.startswith("//"):
        end_idx = input_string.find("\n")
        if end_idx == -1:
            end_idx = len(input_string)
        token = input_string[:end_idx+1]  # incluir el salto de línea
        return token, "COMMENT", len(token)

    best_token = None
    best_action = None
    best_length = 0
    for dfa in dfa_alternatives:
        token, length = simulate_dfa(dfa, input_string)
        if token is not None and length > best_length:
            best_token = token
            best_action = dfa['action']
            best_length = length

    if best_token is None or best_length == 0:
        return None, None, 0

    if best_action == "unified":
        if best_token.startswith('"') and best_token.endswith('"'):
            best_action = "STRING"
        elif best_token.isspace():
            best_action = "NEWLINE" if "\n" in best_token else "WHITESPACE"
        elif best_token in keywords:
            best_action = keywords[best_token]
        elif best_token and (best_token[0].isalpha() or best_token[0] == '_'):
            best_action = "IDENTIFIER"
        elif best_token.isdigit():
            best_action = "INTEGER"
        elif best_token.count('.') == 1 and best_token.replace('.', '').isdigit():
            best_action = "FLOAT"
        else:
            mapping = {
                '+': "PLUS",
                '-': "MINUS",
                '*': "TIMES",
                '/': "DIV",
                '%': "MODULO",
                '==': "EQUAL",
                '!=': "NOT_EQUAL",
                '<': "LESS_THAN",
                '<=': "LESS_EQUAL",
                '>': "GREATER_THAN",
                '>=': "GREATER_EQUAL",
                '=': "ASSIGN",
                ';': "SEMICOLON",
                ',': "COMMA",
                '(': "LPAREN",
                ')': "RPAREN",
                '{': "LBRACE",
                '}': "RBRACE",
                '[': "LBRACKET",
                ']': "RBRACKET"
            }
            best_action = mapping.get(best_token, "UNKNOWN")

    return best_token, best_action, best_length

def scan(input_string):
    tokens = []
    pos = 0
    while pos < len(input_string):
        token, action, advance = get_token(input_string[pos:])
        if token is None or advance == 0:
            raise Exception('Error léxico en: ' + input_string[pos:])
        if action not in ('WHITESPACE', 'NEWLINE'):
            tokens.append((token, action))
        pos += advance
    return tokens


# --- Fin de la generación del analizador léxico ---

# Trailer: Código que se agrega al final del archivo generado
print("Fin de análisis léxico")