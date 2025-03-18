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
        "regex": "whitespace+",
        "action": "return \"WHITESPACE\"",
        "dfa_transitions": {
            "frozenset({frozenset({2, 3})})": {
                ":(\t|\r| )": "frozenset({frozenset({2, 3})})"
            },
            "frozenset({frozenset({1})})": {
                ":(\t|\r| )": "frozenset({frozenset({2, 3})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2, 3})})"
        ]
    },
    {
        "regex": "newline",
        "action": "return \"NEWLINE\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":\n": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "number",
        "action": "return \"INTEGER\"",
        "dfa_transitions": {
            "frozenset({frozenset({2, 3})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({2, 3})})"
            },
            "frozenset({frozenset({1})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({2, 3})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2, 3})})"
        ]
    },
    {
        "regex": "floatnum",
        "action": "return \"FLOAT\"",
        "dfa_transitions": {
            "frozenset({frozenset({5, 6})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({5, 6})})"
            },
            "frozenset({frozenset({2, 3})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({2, 3})})",
                ":.": "frozenset({frozenset({4})})"
            },
            "frozenset({frozenset({1})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({2, 3})})"
            },
            "frozenset({frozenset({4})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({5, 6})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({5, 6})})"
        ]
    },
    {
        "regex": "identifier",
        "action": "if lxm in keywords: return keywords[lxm] return \"IDENTIFIER\"",
        "dfa_transitions": {
            "frozenset({frozenset({2, 3, 4})})": {
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({2, 3, 4})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({2, 3, 4})})"
            },
            "frozenset({frozenset({1})})": {
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({2, 3, 4})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2, 3, 4})})"
        ]
    },
    {
        "regex": "'+'",
        "action": "return \"PLUS\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":+": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'-'",
        "action": "return \"MINUS\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":-": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'*'",
        "action": "return \"TIMES\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":*": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'/'",
        "action": "return \"DIV\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":/": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'%'",
        "action": "return \"MODULO\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":%": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'=='",
        "action": "return \"EQUAL\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":==": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'!='",
        "action": "return \"NOT_EQUAL\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":!=": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'<'",
        "action": "return \"LESS_THAN\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":<": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'<='",
        "action": "return \"LESS_EQUAL\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":<=": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'>'",
        "action": "return \"GREATER_THAN\"",
        "dfa_transitions": {
            "frozenset({frozenset({3})})": {},
            "frozenset({frozenset({1})})": {
                ":": "frozenset({frozenset({2})})"
            },
            "frozenset({frozenset({2})})": {
                ">": "frozenset({frozenset({3})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({3})})"
        ]
    },
    {
        "regex": "'>='",
        "action": "return \"GREATER_EQUAL\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":>=": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'='",
        "action": "return \"ASSIGN\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":=": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "';'",
        "action": "return \"SEMICOLON\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":;": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "','",
        "action": "return \"COMMA\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":,": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'('",
        "action": "return \"LPAREN\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":(": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "')'",
        "action": "return \"RPAREN\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":)": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'{'",
        "action": "return \"LBRACE\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":{": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'}'",
        "action": "return \"RBRACE\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":}": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'['",
        "action": "return \"LBRACKET\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":[": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "']'",
        "action": "return \"RBRACKET\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ":]": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'//' [^\\n]* '\\n'",
        "action": "return \"COMMENT\"",
        "dfa_transitions": {
            "frozenset({frozenset({4})})": {},
            "frozenset({frozenset({1})})": {
                "://": "frozenset({frozenset({2, 3})})"
            },
            "frozenset({frozenset({2, 3})})": {
                "98:(\t|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({2, 3})})",
                ":\n": "frozenset({frozenset({4})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({4})})"
        ]
    },
    {
        "regex": "'/*' ( _ )* '*/'",
        "action": "return \"MULTILINE_COMMENT\"",
        "dfa_transitions": {
            "frozenset({frozenset({4})})": {},
            "frozenset({frozenset({1})})": {
                ":/*": "frozenset({frozenset({2, 3})})"
            },
            "frozenset({frozenset({2, 3})})": {
                "_": "frozenset({frozenset({2, 3})})",
                ":*/": "frozenset({frozenset({4})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({4})})"
        ]
    },
    {
        "regex": "eof",
        "action": "raise(\"Fin de archivo\")",
        "dfa_transitions": {
            "frozenset({frozenset({4})})": {},
            "frozenset({frozenset({2})})": {
                "o": "frozenset({frozenset({3})})"
            },
            "frozenset({frozenset({1})})": {
                "e": "frozenset({frozenset({2})})"
            },
            "frozenset({frozenset({3})})": {
                "f": "frozenset({frozenset({4})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({4})})"
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
        # Caso completo: se espera que tras ':' haya '(' y que termine en ')'
        if i+1 < len(key) and key[i+1] == '(' and key[-1] == ')':
            length_val = 0
            for j in range(i):
                length_val = length_val * 10 + (ord(key[j]) - ord('0'))
            alternatives_str = key[i+2:-1]
            alt_list = alternatives_str.split('|')
            return True, length_val, set(alt_list)
        else:
            # Si no se encuentran los paréntesis, se asume literal de longitud 1
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
    """
    best_token = None
    best_action = None
    best_length = 0
    for dfa in dfa_alternatives:
        token, length = simulate_dfa(dfa, input_string)
        if token is not None and length > best_length:
            best_token = token
            best_action = dfa['action']
            best_length = length
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