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
        except Exception as e:
            print("Error processing expression:", expr)
            print(e)
        print()
