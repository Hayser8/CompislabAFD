#!/usr/bin/env python3
import sys
import importlib
from parser.parser_driver import Parser
from parser.error_recovery import panic_recover
from parser.yalp_parser import YalpParser
from parser.yalp_lexer   import tokenize
from parser.grammar      import Grammar
from lexer.lexeitor      import scan

def main():
    if len(sys.argv) != 4:
        print("Uso: pipeline.py <lexer_module> <grammar.yalp> <source.src>")
        sys.exit(1)

    lexer_mod, yalp_file, src_file = sys.argv[1:]
    # 1) Tokenizamos con el lexer importado
    lex = importlib.import_module(lexer_mod)
    src_text = open(src_file, encoding="utf-8").read()
    tok_pairs = lex.scan(src_text)
    print("\n--- Tokens léxicos ---")
    for lx, tp in tok_pairs:
        print(f"{lx!r} → {tp}")

    # 2) Parseamos .yalp para construir la Grammar
    yalp_text = open(yalp_file, encoding="utf-8").read()
    yalp_toks = list(tokenize(yalp_text))
    grammar: Grammar = YalpParser(yalp_toks).parse()

    # 3) Ejecutamos el parser (con recuperación)
    parser = Parser(grammar)
    ast, errors = parser.parse(tok_pairs)

    # 4) Mostramos resultados
    print("\n--- Errores de sintaxis encontrados ---")
    if errors:
        for e in errors:
            print(e)
    else:
        print("✓ Ningún error de sintaxis.")

    print("\n--- AST resultante ---")
    if ast:
        print(ast)
    else:
        print("∅ (no se pudo construir AST)")

if __name__ == "__main__":
    main()
