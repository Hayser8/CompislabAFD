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

def process_rule(rule_expr, tokens_definitions):
    print("DEBUG: Regla original:", repr(rule_expr))
    
    # Normalización y sustitución de tokens en la expresión
    norm_tokens = {}
    for token_name, token_def in tokens_definitions.items():
        norm_tokens[token_name] = normalize_token_regex(token_def)
    for token_name, token_regex in norm_tokens.items():
        if token_name in rule_expr:
            expanded = recursive_expand(token_regex, norm_tokens)
            print(f"DEBUG: Se encontró token '{token_name}' en la regla; se sustituye por: {expanded}")
            rule_expr = rule_expr.replace(token_name, f"({expanded})")
    
    print("DEBUG: Regla tras sustitución:", repr(rule_expr))
    
    # Eliminar construcciones lookahead (?= ... ) que no soporta el parser.
    # Esta eliminación es segura porque la acción ya está asociada externamente.
    rule_expr = re.sub(r'\(\?\=#.*?\$\#\)', '', rule_expr)
    print("DEBUG: Regla sin lookahead:", repr(rule_expr))
    
    # Si la regla ya está en formato lit(...), se procesa directamente
    if rule_expr.startswith("lit(") and rule_expr.endswith(")"):
        print("DEBUG: La regla es un literal ya formateado, se procesa directamente.")
        tokens = tokenize_postfix(rule_expr)
        print("DEBUG: Tokens obtenidos:", tokens)
        return tokens

    # Preprocesado manual, generación de AST y conversión a notación postfix
    preprocessed = preprocess_expression_manual(rule_expr)
    print("DEBUG: Preprocesada:", repr(preprocessed))
    
    try:
        ast = parse_regex(preprocessed)
        print("DEBUG: AST generado:", ast)
    except Exception as e:
        print("DEBUG: Error al parsear (AST):", e)
        raise
    
    try:
        postfix = to_postfix(ast)
        print("DEBUG: Postfix:", repr(postfix))
    except Exception as e:
        print("DEBUG: Error al convertir a postfix:", e)
        raise
    
    tokens = tokenize_postfix(postfix)
    print("DEBUG: Tokens obtenidos:", tokens)
    return tokens

def integrate_yalex_pipeline(filename, use_minimization=False):
    """
    Integra todo el pipeline a partir del archivo YALex:
     1) Parsear definiciones, tokens, reglas.
     2) Para la regla principal (por ejemplo, "gettoken"), unir todas las alternativas en
        una única expresión regular.
     3) Procesar la expresión unificada para obtener el árbol sintáctico, el DFA (y su versión
        minimizada opcional).
    Devuelve un dict con header, trailer, tokens y rules (con un único DFA para la regla principal).
    """
    # 1. Leer la especificación YALex
    parser = YALexParser(filename)
    header = parser.get_header()
    trailer = parser.get_trailer()
    tokens_definitions = parser.get_tokens()
    rules = parser.get_rules()  # dict con {rule_name: [(regex, action), ...]}

    main_rule = "gettoken"
    if main_rule not in rules or len(rules[main_rule]) == 0:
        raise Exception("No se encontró la regla principal 'gettoken'")

    # 2. Unificar las alternativas de la regla principal
    # Aquí se unen las expresiones con el operador '|' y se agrega un marcador de acción.
    combined_parts = []
    for (regex, action) in rules[main_rule]:
        # Agregar marcador al final de cada alternativa.
        marker = f"(?=#${action}$#)"
        part = f"({regex}){marker}"
        combined_parts.append(part)

    # Se une con el operador de unión '|'
    combined_regex = "|".join(combined_parts)
    print("DEBUG: Expresión regular unificada para 'gettoken':", repr(combined_regex))

    # 3. Procesar la expresión unificada para obtener los tokens, AST y DFA
    try:
        tokens = process_rule(combined_regex, tokens_definitions)
    except Exception as e:
        print(f"DEBUG: Error procesando la expresión unificada {combined_regex}: {e}")
        raise

    # Construir el árbol sintáctico a partir de los tokens obtenidos
    syntax_tree = SyntaxTree(tokens)
    # Construir el DFA a partir del árbol sintáctico
    dfa = DFA(syntax_tree)
    
    # Minimizamos si se solicita
    if use_minimization:
        min_dfa = MinimizedDFA(dfa)
    else:
        min_dfa = None

    # Creamos un único registro para la regla principal
    dfa_unified = {
        "regex": combined_regex,
        "action": "unified",  # Indicamos que se usará descifrado en get_token
        "alternatives": rules[main_rule],  # lista de (regex, action)
        "dfa": dfa,
        "min_dfa": min_dfa
    }

    # Solo se procesa la regla principal de forma unificada.
    dfa_dict = {main_rule: [dfa_unified]}

    return {
        "header": header,
        "trailer": trailer,
        "tokens": tokens_definitions,
        "rules": dfa_dict
    }

if __name__ == '__main__':
    # Ejemplo de invocación del pipeline con el archivo 'lexer.yal'
    # Asegúrate de que exista un archivo 'lexer.yal' en el mismo directorio con la especificación correspondiente.
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
