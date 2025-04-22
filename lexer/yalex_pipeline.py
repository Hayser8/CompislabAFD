from yalex_parser import YALexParser
# Importa el preprocessor manual corregido
from preprocessor import preprocess_expression_manual
from parser import parse_regex, to_postfix
from symbol import Symbol, SymbolType
from arbolSINT import SyntaxTree
from DFA import DFA
from MinimizedDFA import MinimizedDFA
import re

def normalize_token_regex(token_regex):
    """
    Convierte una definición en la forma "['a'-'z' 'A'-'Z' '_']" 
    a la notación estándar "[a-zA-Z_]" eliminando únicamente las comillas.
    """
    if token_regex.startswith("[") and token_regex.endswith("]"):
        inner = token_regex[1:-1]
        inner = inner.replace("'", "")      # <-- quitar solo las comillas
        # NO eliminar espacios aquí: los necesitamos para reconocer ' '
        return f"[{inner}]"
    return token_regex


def recursive_expand(expr, tokens_definitions):
    """
    Reemplaza recursivamente en expr cada ocurrencia de un nombre de token 
    (clave en tokens_definitions) por su definición.
    """
    changed = True
    while changed:
        changed = False
        for token_name, token_def in tokens_definitions.items():
            new_expr = expr.replace(token_name, token_def)
            if new_expr != expr:
                expr = new_expr
                changed = True
    return expr

def tokenize_postfix(postfix_str):
    """
    Tokeniza la notación postfix respetando los literales delimitados por LIT<< ... >>.
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
            i += 6  # omitir "LIT<<"
            literal_chars = []
            while i < n and not postfix_str.startswith(">>", i):
                literal_chars.append(postfix_str[i])
                i += 1
            if i >= n:
                raise ValueError("No se encontró '>>' para token literal iniciado en la posición " + str(start))
            i += 2  # consumir ">>"
            literal_content = "".join(literal_chars)
            literal_converted = bytes(literal_content, "utf-8").decode("unicode_escape")
            tokens.append(Symbol(literal_converted, SymbolType.LITERAL))
        else:
            ch = postfix_str[i]
            if ch in {'*', '|', '·', '+', '?'}:
                tokens.append(Symbol(ch, SymbolType.OPERATOR))
            else:
                tokens.append(Symbol(ch, SymbolType.LITERAL))
            i += 1
    return tokens

def process_rule(rule_expr: str, tokens_definitions: dict[str,str]) -> list[Symbol]:
    """
    1) Expande referencias LET
    2) Preprocesa con preprocess_expression_manual
    3) parse_regex → AST
    4) to_postfix → cadena postfix
    5) tokenize_postfix → lista de Symbol
    """
    print("DEBUG: Regla original:", repr(rule_expr))

    # 1) Expandir LET
    norm = {k: normalize_token_regex(v) for k,v in tokens_definitions.items()}
    for name, rex in norm.items():
        if name in rule_expr:
            exp = recursive_expand(rex, norm)
            print(f"DEBUG: Sustituyendo {name} → {exp}")
            rule_expr = rule_expr.replace(name, f"({exp})")
    print("DEBUG: Tras LET:", repr(rule_expr))

    # 2) No tocamos lookahead marcadores

    # 3) Preprocesar
    pre = preprocess_expression_manual(rule_expr)
    print("DEBUG: Preprocesada:", repr(pre))

    # 4) AST
    ast = parse_regex(pre)
    print("DEBUG: AST generado:", ast)

    # 5) Postfix
    pf = to_postfix(ast)
    print("DEBUG: Postfix:", repr(pf))

    # 6) Tokenizar
    toks = tokenize_postfix(pf)
    print("DEBUG: Tokens:", toks)
    return toks

def integrate_yalex_pipeline(filename: str, use_minimization: bool=False) -> dict:
    """
    Genera todo el pipeline a partir de un .yal:
      - Parser YALex
      - Regex unificada con LIT<<__EOF_i__>>
      - process_rule → Symbols
      - SyntaxTree + DFA(marker_map)
      - (opcional) MinimizedDFA
    Devuelve dict con header, trailer, tokens y rules{"gettoken":[{...}]}
    """
    # 1) Parseo YALex
    parser = YALexParser(filename)
    header = parser.get_header()
    trailer = parser.get_trailer()
    tokens_def = parser.get_tokens()
    rules = parser.get_rules()

    main = "gettoken"
    alternatives = rules.get(main)
    if not alternatives:
        raise RuntimeError(f"No se encontró la regla '{main}'")

    # 2) Construir regex unificada con marcadores
    marker_map: dict[str,str] = {}
    parts: list[str] = []
    for idx,(rex, action) in enumerate(alternatives, start=1):
        mk = f"__EOF_{idx}__"
        marker_map[mk] = action
        parts.append(f"({rex})LIT<<{mk}>>")
    combined_regex = "|".join(parts)
    print("DEBUG: regex unificada:", repr(combined_regex))

    # 3) process_rule → lista de Symbol
    symbols = process_rule(combined_regex, tokens_def)

    # 4) SyntaxTree + DFA
    tree = SyntaxTree(symbols)
    dfa = DFA(tree, marker_map=marker_map)
    min_dfa = MinimizedDFA(dfa) if use_minimization else None

    record = {
        "regex": combined_regex,
        "alternatives": alternatives,   # ← lista [(regex, acción_original), …]
        "action": "unified",            # ← etiqueta que usará generate_lexer_code
        "dfa": dfa,
        "min_dfa": min_dfa
    }

    return {
        "header": header,
        "trailer": trailer,
        "tokens": tokens_def,
        "rules": { main: [record] }
    }

if __name__ == '__main__':
    # Ejemplo de invocación del pipeline con el archivo 'lexer.yal'
    try:
        pipeline_result = integrate_yalex_pipeline("lexer.yal", use_minimization=True)
        print("\n=== Pipeline ejecutado correctamente ===")
        print("Header:")
        print(pipeline_result["header"])
        print("\nTrailer:")
        print(pipeline_result["trailer"])
        print("\nTokens definidos:")
        print(pipeline_result["tokens"])
        print("\nReglas (DFA unificado):")
        print(pipeline_result["rules"])
    except Exception as e:
        print("Ocurrió un error durante la ejecución del pipeline:", e)
