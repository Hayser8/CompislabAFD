# main.py
from preprocessor import preprocess_expression
from parser import parse_regex, to_postfix
from symbol import Symbol
from arbolSINT import SyntaxTree
from DFA import DFA
from MinimizedDFA import MinimizedDFA
import re

def sanitize_filename(name):
    # Reemplaza todo lo que NO sea alfanumérico o un guion bajo por "_"
    return re.sub(r'[^A-Za-z0-9_\-]+', '_', name)

def tokenize_postfix(postfix_str):
    """
    Convierte la cadena en notación postfix (tokens separados por espacios)
    en una lista de objetos Symbol.
    Se asume que:
      - Los operadores son: *, |, ·, ? y +
      - Los literales escapados se generan en el formato: lit(<carácter>)
    """
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

def simulate_dfa(dfa_obj, input_string, minimized=False):
    """
    Simula el DFA dado (original o minimizado) con la cadena de entrada.
    
    Se asume que el DFA fue construido sobre la expresión regular
    concatenada con el símbolo EOF. Por ello, al simular la cadena de entrada
    (sin agregar el EOF) se verifica que el estado resultante sea final,
    es decir, que contenga la posición del símbolo EOF.
    
    Parámetros:
      - dfa_obj: objeto DFA o MinimizedDFA.
      - input_string: cadena de entrada a evaluar.
      - minimized: si es True, se usa la versión minimizada.
    
    Retorna True si la cadena es aceptada, False en caso contrario.
    """
    if minimized:
        transitions = dfa_obj.minimized_transitions
        current_state = dfa_obj.minimized_start
        final_states = dfa_obj.minimized_final
    else:
        transitions = dfa_obj.transitions
        current_state = dfa_obj.start_state
        final_states = dfa_obj.final_states

    # Simular la cadena de entrada sin agregar el símbolo EOF.
    for ch in input_string:
        if current_state in transitions and ch in transitions[current_state]:
            current_state = transitions[current_state][ch]
        else:
            return False
    # Al finalizar, la cadena es aceptada si el estado actual es final.
    return current_state in final_states

if __name__ == "__main__":
    test_expressions = [
        "a+",
        "a?",
        "[0-3]",
        "[ae03]",
        "b+",
        "c?",
        "x+y?",
        "a\\+b",      # Se desea conservar el literal "+"
        "a\\?b",      # Se desea conservar el literal "?"
        "a\\(b\\)",   # Se desean conservar los literales "(" y ")"
        "if\\([ae]+\\)\\{[ei]+\\}(\\\\n(else\\{[jl]+\\}))?",
        "[ae03]+@[ae03]+\\.(com|net|org)(\\.(gt|cr|co))?",
        "{abc}+",
        "a{b}+",
        "((a|b)|(a|b))*abb((a|b)|(a|b))*"
    ]
    
    # Almacenar los DFAs generados para cada expresión
    dfa_results = []  # Cada elemento: (expr, dfa, min_dfa)

    for expr in test_expressions:
        try:
            print("--------------------------------------------------")
            print("Infix:       ", expr)
            preprocessed = preprocess_expression(expr)
            print("Preprocessed:", repr(preprocessed))
            
            # Construir el AST y la notación postfix.
            ast = parse_regex(preprocessed)
            postfix = to_postfix(ast)
            print("Postfix:     ", postfix)
            
            # Tokenizar y construir el árbol sintáctico.
            tokens = tokenize_postfix(postfix)
            syntax_tree = SyntaxTree(tokens)
            
            # Construir y visualizar el DFA
            dfa = DFA(syntax_tree)
            filename_dfa = "dfa_" + sanitize_filename(expr)
            dfa.visualize(filename_dfa)
            print("DFA image generated:", filename_dfa + ".png")
            
            # Construir y visualizar el DFA minimizado
            min_dfa = MinimizedDFA(dfa)
            filename_min = "min_dfa_" + sanitize_filename(expr)
            min_dfa.visualize(filename_min)
            print("Minimized DFA image generated:", filename_min + ".png")
            
            # Guardar resultados para simulación posterior.
            dfa_results.append((expr, dfa, min_dfa))
        except Exception as e:
            print("Error processing expression:", expr)
            print(e)
        print()
    
    # Si se procesó al menos una expresión, preguntar si se desea simular alguna.
    if dfa_results:
        simulate_choice = input("¿Desea simular alguna de las expresiones procesadas? (s/n): ").strip().lower()
        if simulate_choice == 's':
            print("\nExpresiones procesadas:")
            for idx, (expr, _, _) in enumerate(dfa_results):
                print(f"{idx}: {expr}")
            try:
                index = int(input("Ingrese el número de la expresión a simular: "))
                if index < 0 or index >= len(dfa_results):
                    raise ValueError("Índice fuera de rango")
            except Exception as e:
                print("Índice inválido. Se usará la última expresión procesada.")
                index = len(dfa_results) - 1
            input_string = input("Ingrese la cadena a simular: ")
            expr, dfa, min_dfa = dfa_results[index]
            accepted_orig = simulate_dfa(dfa, input_string, minimized=False)
            accepted_min = simulate_dfa(min_dfa, input_string, minimized=True)
            print("\nResultados de la simulación para la expresión:", expr)
            print(f"La cadena '{input_string}' es {'válida' if accepted_orig else 'inválida'} según el DFA original.")
            print(f"La cadena '{input_string}' es {'válida' if accepted_min else 'inválida'} según el DFA minimizado.")
