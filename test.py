import sys
from lexeitor import scan, get_token


archivo_entrada = "test5.txt"
with open(archivo_entrada, "r", encoding="utf-8") as f:
    test_input = f.read()


try:
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        test_input = f.read()
except Exception as e:
    print(f"Error al abrir el archivo {archivo_entrada}: {e}")
    sys.exit(1)

# Normalizar saltos de línea
test_input = test_input.replace("\r\n", "\n").replace("\r", "")

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
