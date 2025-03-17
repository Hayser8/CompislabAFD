from yalex_parser import YALexParser
# Importa el preprocessor manual en lugar del original
from preprocessor import preprocess_expression_manual  
from parser import parse_regex, to_postfix
from symbol import Symbol
from arbolSINT import SyntaxTree
from DFA import DFA
from MinimizedDFA import MinimizedDFA

def normalize_token_regex(token_regex):
    """
    Convierte una definición en la forma "['a'-'z' 'A'-'Z' '_']" 
    a la notación estándar "[a-zA-Z_]" eliminando comillas y espacios.
    """
    if token_regex.startswith("[") and token_regex.endswith("]"):
        inner = token_regex[1:-1]
        # Elimina comillas y espacios
        inner = inner.replace("'", "").replace(" ", "")
        return f"[{inner}]"
    return token_regex

def recursive_expand(expr, tokens_definitions):
    """
    Reemplaza recursivamente en expr cada ocurrencia de un nombre de token (clave en tokens_definitions)
    por su definición. Se usa un simple while con str.replace, sin usar re.
    """
    changed = True
    # Repite hasta que no haya cambios
    while changed:
        changed = False
        for token_name, token_def in tokens_definitions.items():
            # Si se encuentra el nombre del token en la expresión,
            # se reemplaza por su definición
            new_expr = expr.replace(token_name, token_def)
            if new_expr != expr:
                expr = new_expr
                changed = True
    return expr

def tokenize_postfix(postfix_str):
    tokens = postfix_str.split()
    result = []
    for token in tokens:
        if token.startswith("lit(") and token.endswith(")"):
            literal_char = token[4:-1]
            result.append(Symbol(literal_char, "operand"))
        elif token in {'*', '|', '·', '?', '+'}:
            result.append(Symbol(token, "operator"))
        else:
            result.append(Symbol(token, "operand"))
    return result

def process_rule(rule_expr, tokens_definitions):
    """
    Procesa la cadena de la expresión regular extraída de la regla:
      - Si la regla es un literal entre comillas, se le quitan las comillas.
      - Si la regla es exactamente el nombre de un token definido, se reemplaza recursivamente por su definición.
      - Si la regla contiene nombres de tokens, se sustituyen por sus definiciones.
      - Luego se preprocesa, se parsea y se convierte a notación postfix.
    Devuelve la lista de tokens.
    """
    print("DEBUG: Regla original:", repr(rule_expr))
    literal_tokens = {'+', '-', '*', '/', '%', '=', '==', '!=', '<', '<=', '>', '>=' , '(', ')', '{', '}', '[', ']'}
    
    # Si es un literal entre comillas, quita las comillas y, si es un operador o símbolo, lo formatea
    if rule_expr.startswith("'") and rule_expr.endswith("'"):
        rule_expr = rule_expr[1:-1]
        print("DEBUG: Se quitaron las comillas:", repr(rule_expr))
        if rule_expr in literal_tokens:
            rule_expr = f"lit({rule_expr})"
            print("DEBUG: Literal operator convertido a:", repr(rule_expr))
    
    # Si la regla es exactamente el nombre de un token definido, se expande recursivamente
    if rule_expr.strip() in tokens_definitions:
        rule_expr = recursive_expand(tokens_definitions[rule_expr.strip()], tokens_definitions)
    else:
        # Sino, se sustituyen todas las ocurrencias de tokens definidos en la regla
        for token_name, token_regex in tokens_definitions.items():
            if token_name in rule_expr:
                expanded = recursive_expand(token_regex, tokens_definitions)
                print(f"DEBUG: Se encontró token '{token_name}' en la regla; se sustituye por: {expanded}")
                rule_expr = rule_expr.replace(token_name, f"({expanded})")
    print("DEBUG: Regla tras sustitución:", repr(rule_expr))
    
    # Si la regla ya está en formato lit(...), se procesa directamente
    if rule_expr.startswith("lit(") and rule_expr.endswith(")"):
        print("DEBUG: La regla es un literal ya formateado, se procesa directamente.")
        tokens = tokenize_postfix(rule_expr)
        print("DEBUG: Tokens obtenidos:", tokens)
        return tokens
    
    # Se utiliza el nuevo preprocessor manual para mejorar el rendimiento con entradas grandes
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
    Integra todo el pipeline a partir del archivo YALex.
    Retorna un diccionario con:
      - header y trailer del archivo YALex.
      - tokens: definiciones de tokens.
      - rules: para cada regla se construyen el DFA y, si se solicita, el DFA minimizado.
    """
    # 1. Leer la especificación YALex
    parser = YALexParser(filename)
    header = parser.get_header()
    trailer = parser.get_trailer()
    tokens_definitions = parser.get_tokens()
    rules = parser.get_rules()  # Ej: {'gettoken': [(regex, action), ...]}
    
    # 2. Procesar cada regla y construir el DFA (y DFA minimizado, opcional)
    dfa_dict = {}
    for rule_name, rule_list in rules.items():
        for (regex, action) in rule_list:
            print("\nDEBUG: Procesando regla para", rule_name)
            print("DEBUG: Expresión original:", repr(regex))
            try:
                tokens = process_rule(regex, tokens_definitions)
            except Exception as e:
                print(f"DEBUG: Error procesando la regla {regex}: {e}")
                raise
            syntax_tree = SyntaxTree(tokens)
            dfa = DFA(syntax_tree)
            if use_minimization:
                min_dfa = MinimizedDFA(dfa)
            else:
                min_dfa = None
            dfa_dict.setdefault(rule_name, []).append({
                "regex": regex,
                "action": action,
                "dfa": dfa,
                "min_dfa": min_dfa
            })
    
    return {
        "header": header,
        "trailer": trailer,
        "tokens": tokens_definitions,
        "rules": dfa_dict
    }

if __name__ == "__main__":
    # Configuración: Cambia a True si deseas generar y visualizar el DFA minimizado.
    use_minimization = True
    
    pipeline_result = integrate_yalex_pipeline("lexer.yal", use_minimization)
    
    print("Header:")
    print(pipeline_result["header"])
    print("\nRules:")
    for rule, dfa_list in pipeline_result["rules"].items():
        print(f"Regla {rule}:")
        for item in dfa_list:
            print("  Regex:", item["regex"])
            print("  Action:", item["action"])
            print("  Visualizando DFA:")
            item["dfa"].visualize(f"dfa_{rule}")
            if item["min_dfa"] is not None:
                print("  Visualizando DFA Minimized:")
                item["min_dfa"].visualize(f"min_dfa_{rule}")
    print("\nTrailer:")
    print(pipeline_result["trailer"])
