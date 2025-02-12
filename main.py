from preprocessor import preprocess_expression
from parser import parse_regex, to_postfix
from symbol import Symbol
from arbolSINT import SyntaxTree
from DFA import DFA

def tokenize_postfix(postfix_str):
    """
    Convierte la cadena postfix (tokens separados por espacios) en una lista de objetos Symbol.
    Se asume que los operadores son: *, |, ·, ?, +
    """
    tokens = postfix_str.split()
    result = []
    for token in tokens:
        # Si el token comienza con '§', se trata como literal escapado.
        if token.startswith("§"):
            result.append(Symbol(token[1:], "operand"))
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
        "x+ y?",
        "a\\+b",      # Se desea conservar el literal "+"
        "a\\?b",      # Se desea conservar el literal "?"
        "a\\(b\\)",   # Se desean conservar los literales "(" y ")"
        "if\\([ae] +\\)\\{[ei] +\\}(\\n(else\\{[jl] +\\}))?",
        "[ae03]+@[ae03]+\\.(com|net|org)(\\.(gt|cr|co))?",
        "{abc}+",
        "a{b}+"
    ]
    
    for expr in test_expressions:
        try:
            print("--------------------------------------------------")
            print("Infix:       ", expr)
            preprocessed = preprocess_expression(expr)
            print("Preprocessed:", repr(preprocessed))
            ast = parse_regex(preprocessed)
            postfix = to_postfix(ast)
            print("Postfix:     ", postfix)
            tokens = tokenize_postfix(postfix)
            syntax_tree = SyntaxTree(tokens)
            dfa = DFA(syntax_tree)
            print("DFA transitions:", dfa.transitions)
            print("Final states:   ", dfa.final_states)
            # Se genera la imagen del DFA usando la notación infix original como nombre de archivo.
            dfa.visualize(expr)
            print(f"DFA image generated: {expr}")
        except Exception as e:
            print("Error processing expression:", expr)
            print(e)
        print()
