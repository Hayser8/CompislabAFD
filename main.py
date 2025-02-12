from preprocessor import preprocess_expression
from parser import parse_regex, to_postfix

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
        "[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?",
        "{abc}+",
        "a{b}+"
    ]
    
    for expr in test_expressions:
        try:
            preprocessed = preprocess_expression(expr)
            ast = parse_regex(preprocessed)
            postfix = to_postfix(ast)
            print("Infix:       ", expr)
            print("Preprocessed:", repr(preprocessed))
            print("Postfix:     ", postfix)
            print()
        except Exception as e:
            print("Infix:       ", expr)
            print("Error:       ", e)
            print()
