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
            "frozenset({frozenset({25, 13})})": {
                "[": "frozenset({frozenset({2}), frozenset({14})})"
            },
            "frozenset({frozenset({9}), frozenset({21})})": {
                "\\": "frozenset({frozenset({10}), frozenset({22})})"
            },
            "frozenset({frozenset({5}), frozenset({17})})": {
                "\\": "frozenset({frozenset({18}), frozenset({6})})"
            },
            "frozenset({frozenset({1})})": {
                "[": "frozenset({frozenset({2}), frozenset({14})})"
            },
            "frozenset({frozenset({18}), frozenset({6})})": {
                "t": "frozenset({frozenset({19}), frozenset({7})})"
            },
            "frozenset({frozenset({23}), frozenset({11})})": {
                "'": "frozenset({frozenset({24}), frozenset({12})})"
            },
            "frozenset({frozenset({16}), frozenset({4})})": {
                "'": "frozenset({frozenset({5}), frozenset({17})})"
            },
            "frozenset({frozenset({3}), frozenset({15})})": {
                "'": "frozenset({frozenset({16}), frozenset({4})})"
            },
            "frozenset({frozenset({2}), frozenset({14})})": {
                "'": "frozenset({frozenset({3}), frozenset({15})})"
            },
            "frozenset({frozenset({20}), frozenset({8})})": {
                "'": "frozenset({frozenset({9}), frozenset({21})})"
            },
            "frozenset({frozenset({19}), frozenset({7})})": {
                "'": "frozenset({frozenset({20}), frozenset({8})})"
            },
            "frozenset({frozenset({10}), frozenset({22})})": {
                "r": "frozenset({frozenset({23}), frozenset({11})})"
            },
            "frozenset({frozenset({24}), frozenset({12})})": {
                "]": "frozenset({frozenset({25, 13})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({25, 13})})"
        ]
    },
    {
        "regex": "newline",
        "action": "return \"NEWLINE\"",
        "dfa_transitions": {
            "frozenset({frozenset({4})})": {},
            "frozenset({frozenset({1})})": {
                "'": "frozenset({frozenset({2})})"
            },
            "frozenset({frozenset({2})})": {
                "n": "frozenset({frozenset({3})})"
            },
            "frozenset({frozenset({3})})": {
                "'": "frozenset({frozenset({4})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({4})})"
        ]
    },
    {
        "regex": "number",
        "action": "return \"INTEGER\"",
        "dfa_transitions": {
            "frozenset({frozenset({6, 7})})": {
                "t": "frozenset({frozenset({6, 7})})"
            },
            "frozenset({frozenset({2})})": {
                "i": "frozenset({frozenset({3})})"
            },
            "frozenset({frozenset({4})})": {
                "i": "frozenset({frozenset({5})})"
            },
            "frozenset({frozenset({1})})": {
                "d": "frozenset({frozenset({2})})"
            },
            "frozenset({frozenset({3})})": {
                "g": "frozenset({frozenset({4})})"
            },
            "frozenset({frozenset({5})})": {
                "t": "frozenset({frozenset({6, 7})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({6, 7})})"
        ]
    },
    {
        "regex": "floatnum",
        "action": "return \"FLOAT\"",
        "dfa_transitions": {
            "frozenset({frozenset({16, 15})})": {
                "t": "frozenset({frozenset({16, 15})})"
            },
            "frozenset({frozenset({8})})": {
                ".": "frozenset({frozenset({9})})"
            },
            "frozenset({frozenset({1})})": {
                "d": "frozenset({frozenset({2})})"
            },
            "frozenset({frozenset({10})})": {
                "d": "frozenset({frozenset({11})})"
            },
            "frozenset({frozenset({6, 7})})": {
                "t": "frozenset({frozenset({6, 7})})",
                "'": "frozenset({frozenset({8})})"
            },
            "frozenset({frozenset({5})})": {
                "t": "frozenset({frozenset({6, 7})})"
            },
            "frozenset({frozenset({9})})": {
                "'": "frozenset({frozenset({10})})"
            },
            "frozenset({frozenset({12})})": {
                "g": "frozenset({frozenset({13})})"
            },
            "frozenset({frozenset({3})})": {
                "g": "frozenset({frozenset({4})})"
            },
            "frozenset({frozenset({13})})": {
                "i": "frozenset({frozenset({14})})"
            },
            "frozenset({frozenset({2})})": {
                "i": "frozenset({frozenset({3})})"
            },
            "frozenset({frozenset({11})})": {
                "i": "frozenset({frozenset({12})})"
            },
            "frozenset({frozenset({4})})": {
                "i": "frozenset({frozenset({5})})"
            },
            "frozenset({frozenset({14})})": {
                "t": "frozenset({frozenset({16, 15})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({16, 15})})"
        ]
    },
    {
        "regex": "identifier",
        "action": "if lxm in keywords: return keywords[lxm] return \"IDENTIFIER\"",
        "dfa_transitions": {
            "frozenset({frozenset({18, 13, 7})})": {
                "d": "frozenset({frozenset({14})})",
                "l": "frozenset({frozenset({2}), frozenset({8})})"
            },
            "frozenset({frozenset({2}), frozenset({8})})": {
                "e": "frozenset({frozenset({9}), frozenset({3})})"
            },
            "frozenset({frozenset({5}), frozenset({11})})": {
                "e": "frozenset({frozenset({6}), frozenset({12})})"
            },
            "frozenset({frozenset({9}), frozenset({3})})": {
                "t": "frozenset({frozenset({10}), frozenset({4})})"
            },
            "frozenset({frozenset({10}), frozenset({4})})": {
                "t": "frozenset({frozenset({5}), frozenset({11})})"
            },
            "frozenset({frozenset({1})})": {
                "l": "frozenset({frozenset({2}), frozenset({8})})"
            },
            "frozenset({frozenset({14})})": {
                "i": "frozenset({frozenset({15})})"
            },
            "frozenset({frozenset({16})})": {
                "i": "frozenset({frozenset({17})})"
            },
            "frozenset({frozenset({15})})": {
                "g": "frozenset({frozenset({16})})"
            },
            "frozenset({frozenset({17})})": {
                "t": "frozenset({frozenset({18, 13, 7})})"
            },
            "frozenset({frozenset({6}), frozenset({12})})": {
                "r": "frozenset({frozenset({18, 13, 7})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({18, 13, 7})})"
        ]
    },
    {
        "regex": "'+'",
        "action": "return \"PLUS\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                "+": "frozenset({frozenset({2})})"
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
                "-": "frozenset({frozenset({2})})"
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
                "*": "frozenset({frozenset({2})})"
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
                "/": "frozenset({frozenset({2})})"
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
                "%": "frozenset({frozenset({2})})"
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
                "==": "frozenset({frozenset({2})})"
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
                "!=": "frozenset({frozenset({2})})"
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
                "<": "frozenset({frozenset({2})})"
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
                "<=": "frozenset({frozenset({2})})"
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
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ">": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'>='",
        "action": "return \"GREATER_EQUAL\"",
        "dfa_transitions": {
            "frozenset({frozenset({2})})": {},
            "frozenset({frozenset({1})})": {
                ">=": "frozenset({frozenset({2})})"
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
                "=": "frozenset({frozenset({2})})"
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
                ";": "frozenset({frozenset({2})})"
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
                ",": "frozenset({frozenset({2})})"
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
                "(": "frozenset({frozenset({2})})"
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
                ")": "frozenset({frozenset({2})})"
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
                "{": "frozenset({frozenset({2})})"
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
                "}": "frozenset({frozenset({2})})"
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
                "[": "frozenset({frozenset({2})})"
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
                "]": "frozenset({frozenset({2})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({2})})"
        ]
    },
    {
        "regex": "'//' .* '\\n'",
        "action": "return \"COMMENT\"",
        "dfa_transitions": {
            "frozenset({frozenset({7})})": {},
            "frozenset({frozenset({4, 5})})": {
                ".": "frozenset({frozenset({4, 5})})",
                "'": "frozenset({frozenset({6})})"
            },
            "frozenset({frozenset({3})})": {
                "'": "frozenset({frozenset({4, 5})})"
            },
            "frozenset({frozenset({2})})": {
                "/": "frozenset({frozenset({3})})"
            },
            "frozenset({frozenset({1})})": {
                "/": "frozenset({frozenset({2})})"
            },
            "frozenset({frozenset({6})})": {
                "n": "frozenset({frozenset({7})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1})})",
        "dfa_final": [
            "frozenset({frozenset({7})})"
        ]
    },
    {
        "regex": "'/*' ( _ )* '*/'",
        "action": "return \"MULTILINE_COMMENT\"",
        "dfa_transitions": {
            "frozenset({frozenset({6})})": {},
            "frozenset({frozenset({1, 2})})": {
                "/": "frozenset({frozenset({1, 2})})",
                "'": "frozenset({frozenset({3, 4, 5})})"
            },
            "frozenset({frozenset({3, 4, 5})})": {
                "_": "frozenset({frozenset({3, 4, 5})})",
                "'": "frozenset({frozenset({4, 5})})",
                "/": "frozenset({frozenset({6})})"
            },
            "frozenset({frozenset({4, 5})})": {
                "'": "frozenset({frozenset({4, 5})})",
                "/": "frozenset({frozenset({6})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1, 2})})",
        "dfa_final": [
            "frozenset({frozenset({6})})"
        ]
    },
    {
        "regex": "eof",
        "action": "raise(\"Fin de archivo\")",
        "dfa_transitions": {
            "frozenset({frozenset({4})})": {},
            "frozenset({frozenset({1})})": {
                "e": "frozenset({frozenset({2})})"
            },
            "frozenset({frozenset({2})})": {
                "o": "frozenset({frozenset({3})})"
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


def simulate_dfa(dfa, input_string):
    """
    Simula el DFA dado (representado por un diccionario con:
      - dfa_transitions: dict con claves de estado (str) y valores dict {symbol: target_state (str)}
      - dfa_start: estado inicial (str)
      - dfa_final: lista de estados finales (str)
    ) sobre la cadena input_string.
    Retorna (token, advance) si se reconoce un token, o (None, 0) en caso contrario.
    """
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
            best_action = dfa["action"]
            best_length = length
    return best_token, best_action, best_length

def scan(input_string):
    """
    Función principal del analizador léxico. Recorre la cadena de entrada extrayendo tokens y sus acciones.
    Retorna una lista de tuplas (token, action).
    """
    tokens = []
    pos = 0
    while pos < len(input_string):
        token, action, advance = get_token(input_string[pos:])
        if token is None or advance == 0:
            raise Exception("Error léxico en: " + input_string[pos:])
        tokens.append((token, action))
        pos += advance
    return tokens


# --- Fin de la generación del analizador léxico ---

# Trailer: Código que se agrega al final del archivo generado
print("Fin de análisis léxico")