from yalp_lexer import tokenize
from yalp_parser import YalpParser
from first_follow import FirstFollowCalculator
from lr0 import build_canonical

# 1. Leer archivo yalp de prueba
with open("./parser/test.yalp", encoding="utf-8") as f:
    text = f.read()

# 2. Tokenizar
tokens = list(tokenize(text))

# 3. Parsear
parser = YalpParser(tokens)
grammar = parser.parse()

# 4. Calcular FIRST/FOLLOW
calculator = FirstFollowCalculator(grammar)

print("=== TERMINALES ===")
for t in sorted(grammar.terminals, key=str):
    print(f"  {t}")

print("\n=== NO TERMINALES ===")
for nt in sorted(grammar.non_terminals, key=str):
    print(f"  {nt}")

print("\n=== PRODUCCIONES ===")
for p in grammar.productions:
    print(f"  {p.head} → {' '.join(str(sym) for sym in p.body)}")

print("\n=== FIRST ===")
for nt in sorted(grammar.non_terminals, key=str):
    first_set = calculator.get_first(nt)
    print(f"  FIRST({nt}): {{{', '.join(map(str, sorted(first_set, key=str)))}}}")

print("\n=== FOLLOW ===")
for nt in sorted(grammar.non_terminals, key=str):
    follow_set = calculator.get_follow(nt)
    print(f"  FOLLOW({nt}): {{{', '.join(map(str, sorted(follow_set, key=str)))}}}")

# 5. Construcción del conjunto canónico de estados LR(0)
print("\n=== CONJUNTO CANÓNICO DE ESTADOS LR(0) ===")
states = build_canonical(grammar)

for state in states:
    print(f"\n{state}")
