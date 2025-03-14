from yalex_parser import YALexParser
from preprocessor import preprocess_expression
from parser import parse_regex, to_postfix
from symbol import Symbol
from arbolSINT import SyntaxTree
from DFAG import DFAG
from minimizer import MinimizedDFA
# Si deseas usar DFA minimizado, también importas MinimizedDFA

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
    Toma la cadena de la expresión regular extraída de la regla,
    realiza la sustitución de nombres de tokens definidos,
    la preprocesa, la convierte a AST y luego a notación postfix.
    Devuelve la lista de tokens.
    """
    print("DEBUG: Regla original:", repr(rule_expr))
    # Conjunto de literales que queremos tratar como literales (no como operadores de agrupación)
    literal_tokens = {'+', '-', '*', '/', '%', '=', '==', '!=', '<', '<=', '>', '>=' , '(', ')', '{', '}', '[', ']'}
    
    # Si la regla es un literal encerrado entre comillas simples, quitarlas.
    if rule_expr.startswith("'") and rule_expr.endswith("'"):
        rule_expr = rule_expr[1:-1]
        print("DEBUG: Se quitaron las comillas:", repr(rule_expr))
        if rule_expr in literal_tokens:
            # Para operadores y símbolos, lo convertimos a formato lit(...)
            rule_expr = f"lit({rule_expr})"
            print("DEBUG: Literal operator convertido a:", repr(rule_expr))
    
    # Sustitución de tokens definidos
    for token_name, token_regex in tokens_definitions.items():
        if rule_expr.strip() == token_name:
            print(f"DEBUG: La regla coincide exactamente con token '{token_name}', se reemplaza por su definición.")
            rule_expr = token_regex
        else:
            if token_name in rule_expr:
                print(f"DEBUG: Se encontró token '{token_name}' en la regla; se sustituye por: {token_regex}")
                rule_expr = rule_expr.replace(token_name, f"({token_regex})")
    print("DEBUG: Regla tras sustitución:", repr(rule_expr))
    
    # Si ya está en formato lit(...), procesarlo directamente sin pasar por el parser
    if rule_expr.startswith("lit(") and rule_expr.endswith(")"):
        print("DEBUG: La regla es un literal ya formateado, se procesa directamente.")
        tokens = tokenize_postfix(rule_expr)
        print("DEBUG: Tokens obtenidos:", tokens)
        return tokens

    preprocessed = preprocess_expression(rule_expr)
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

def integrate_yalex_pipeline(filename):
    """
    Integra todo el pipeline a partir del archivo YALex.
    Retorna un diccionario con:
      - tokens: definiciones (let)
      - reglas: cada regla con su DFA generado
      - header y trailer
    """
    # 1. Leer la especificación YALex
    parser = YALexParser(filename)
    
    # Extraer header, trailer, tokens y reglas
    header = parser.get_header()
    trailer = parser.get_trailer()
    tokens_definitions = parser.get_tokens()
    rules = parser.get_rules()  # Ej: {'gettoken': [(regex, action), ...]}
    
    # 2. Para cada regla, procesa la expresión regular y construye el árbol y DFA.
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
            dfa = DFAG(syntax_tree)
            # minimizado
            min_dfa = MinimizedDFA(dfa)
            
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
    # 1. Ejecuta el pipeline y obtiene el resultado
    pipeline_result = integrate_yalex_pipeline("lexer.yal")

    # 2. Imprime el header
    print("Header:")
    print(pipeline_result["header"])
    
    # 3. Recorre las reglas encontradas
    print("\nRules:")
    for rule, dfa_list in pipeline_result["rules"].items():
        print(f"Regla {rule}:")
        for item in dfa_list:
            print("  Regex:", item["regex"])
            print("  Action:", item["action"])
            
            # 'dfa' es la instancia de DFAG devuelta en el diccionario
            # Se llama el método visualize en esa instancia
            item["dfa"].visualize(f"dfa_{rule}")

            # 'min_dfa' es la instancia de MinimizedDFA
            # También posee el método visualize
            item["min_dfa"].visualize(f"dfa_min_{rule}")
            
    # 4. Imprime el trailer
    print("\nTrailer:")
    print(pipeline_result["trailer"])

