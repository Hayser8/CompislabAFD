# main_pipeline.py

from yalex_parser import YALexParser
# Importa el preprocessor manual corregido
from preprocessor import preprocess_expression_manual
from parser import parse_regex, to_postfix
from symbol import Symbol, SymbolType
from arbolSINT import SyntaxTree
from DFA import DFA
from MinimizedDFA import MinimizedDFA

def normalize_token_regex(token_regex):
    """
    Convierte una definición en la forma "['a'-'z' 'A'-'Z' '_']" 
    a la notación estándar "[a-zA-Z_]" eliminando comillas y espacios.
    (Opcional, depende de tus necesidades)
    """
    if token_regex.startswith("[") and token_regex.endswith("]"):
        inner = token_regex[1:-1]
        # Elimina comillas y espacios
        inner = inner.replace("'", "").replace(" ", "")
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

    # 1) Si la expresión está completamente entrecomillada Y NO contiene espacios
    # (es decir, es un único carácter o una secuencia sin espacios) se asume que es literal.
    if rule_expr.startswith("'") and rule_expr.endswith("'") and (' ' not in rule_expr):
        inner = rule_expr[1:-1]  # contenido entre comillas
        # Si el usuario desea escapar el carácter, por ejemplo "'\\('" para literal "(",
        # se detecta la barra invertida.
        if rule_expr.startswith("'") and rule_expr.endswith("'") and (' ' not in rule_expr):
            inner = rule_expr[1:-1]
            if inner and inner[0] == '\\':
                inner = inner[1:]
                print(f"DEBUG: Se detectó escape, literal: {inner!r}")
                rule_expr = f"LIT<<{inner}>>"
                print(f"DEBUG: Literal operator convertido a: {rule_expr!r}")
            elif len(inner) == 1:
                print(f"DEBUG: Se quitaron las comillas: {inner!r}")
                rule_expr = f"LIT<<{inner}>>"
                print(f"DEBUG: Literal operator convertido a: {rule_expr!r}")
            else:
                print(f"DEBUG: Es una expresión compleja o literal extendido, se conservan comillas: {inner!r}")


    
    # 2) Expansión recursiva: si rule_expr coincide exactamente con el nombre de un token, se expande
    if rule_expr.strip() in tokens_definitions:
        rule_expr = recursive_expand(tokens_definitions[rule_expr.strip()], tokens_definitions)
    else:
        # O sustitución parcial: se reemplazan ocurrencias de nombres de tokens por sus definiciones
        for token_name, token_regex in tokens_definitions.items():
            if token_name in rule_expr:
                expanded = recursive_expand(token_regex, tokens_definitions)
                print(f"DEBUG: Se encontró token '{token_name}' en la regla; se sustituye por: {expanded}")
                rule_expr = rule_expr.replace(token_name, f"({expanded})")
    print("DEBUG: Regla tras sustitución:", repr(rule_expr))
    
    # 3) Si la regla ya quedó en formato lit(...), se procesa directamente
    if rule_expr.startswith("lit(") and rule_expr.endswith(")"):
        print("DEBUG: La regla es un literal ya formateado, se procesa directamente.")
        tokens = tokenize_postfix(rule_expr)
        print("DEBUG: Tokens obtenidos:", tokens)
        return tokens
    
    # 4) Preprocesado manual, AST y conversión a postfix (resto sin cambios)
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
     2) Para cada regla, obtener postfix y SyntaxTree.
     3) Construir DFA (y minimizado opcional).
    Devuelve un dict con header, trailer, tokens y rules (cada una con su DFA).
    """
    # 1. Leer la especificación YALex
    parser = YALexParser(filename)
    header = parser.get_header()
    trailer = parser.get_trailer()
    tokens_definitions = parser.get_tokens()
    rules = parser.get_rules()  # dict con {rule_name: [(regex, action), ...]}
    
    # 2. Procesar cada regla y construir el DFA
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
            
            # Construir el árbol sintáctico
            syntax_tree = SyntaxTree(tokens)
            # Construir el DFA
            dfa = DFA(syntax_tree)
            
            # Minimizamos si se solicita
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


