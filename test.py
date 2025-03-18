from thelexer import scan, get_token

# Entrada de prueba compleja: combina estructuras de control, operaciones, bloques y comentarios.
test_input = (
    "if (x + 10) {\r\n"
    "    // Esto es un comentario de linea\r\n"
    "    return x;\r\n"
    "} else {\r\n"
    "    /* Comentario de bloque\r\n"
    "       que abarca varias lineas */\r\n"
    "    return 0;\r\n"
    "}\r\n"
    "while (count <= 100) { count = count + 1; }\r\n"
)

# -- AQUÍ normalizamos los saltos de línea Windows a Unix --
test_input = test_input.replace("\r\n", "\n")  # si la entrada tenía CR+LF
test_input = test_input.replace("\r", "")      # por si quedara algún CR solitario

print("Analizando entrada completa:")
print(test_input)
print("\n--- Tokens obtenidos ---")

i = 0
while i < len(test_input):
    tk, act, adv = get_token(test_input[i:])
    if tk is None or adv == 0:
        raise Exception(f"Error léxico en: {test_input[i:]}")
    print(f"Entrada: {test_input[i:i+adv]!r} -> {tk!r}, {act!r}, adv: {adv}")
    i += adv

print("\nFin de análisis léxico")
