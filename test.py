from thelexer import scan

# Cadena de prueba simple que solo usa tokens reconocidos: LPAREN, PLUS, RPAREN y SEMICOLON.
input_string = "(+);"

try:
    tokens = scan(input_string)
    print("Tokens reconocidos:", tokens)
except Exception as e:
    print("Error durante el análisis:", e)
