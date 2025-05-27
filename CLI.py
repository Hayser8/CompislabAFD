#!/usr/bin/env python3
# cli.py
"""
CLI para YALex + YAPar:
  1) Léxico
  2) Sintáctico (+ recuperación de errores)
  3) Impresión de tokens, errores y AST
"""

import sys
import os
import argparse
import importlib

def main():
    p = argparse.ArgumentParser(
        description="YALex + YAPar CLI: léxico, sintáctico y AST"
    )
    p.add_argument("lexer_module", help="Módulo Python del lexer (p.ej. 'lexeitor')")
    p.add_argument("grammar_yalp", help="Archivo .yalp con la gramática YAPar")
    p.add_argument("source_file",  help="Archivo de código fuente a analizar")
    args = p.parse_args()

    sys.path.insert(0, os.getcwd())

    # 1) Cargar lexer
    try:
        lex = importlib.import_module(args.lexer_module)
    except ImportError as e:
        print(f"[CLI ERROR] No puedo importar '{args.lexer_module}': {e}")
        sys.exit(1)

    # 2) Tokenizar y parsear la gramática
    from parser.yalp_lexer    import tokenize as yalp_tokenize
    from parser.yalp_parser   import YalpParser
    from parser.parser_driver import Parser, ParseError

    try:
        yalp_txt = open(args.grammar_yalp, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"[CLI ERROR] Gramática no encontrada: '{args.grammar_yalp}'")
        sys.exit(1)

    yalp_toks = list(yalp_tokenize(yalp_txt))
    try:
        grammar = YalpParser(yalp_toks).parse()
    except Exception as e:
        print(f"[CLI ERROR] Error parseando gramática: {e}")
        sys.exit(1)

    # 3) Leer fuente y hacer léxico
    try:
        src = open(args.source_file, encoding="utf-8").read()
        src = src.replace("\r\n", "\n").replace("\r", "\n")
    except FileNotFoundError:
        print(f"[CLI ERROR] Fuente no encontrada: '{args.source_file}'")
        sys.exit(1)

    print("=== ANÁLISIS LÉXICO ===")
    try:
        tokens = lex.scan(src)
    except lex.LexerError as e:
        print(f"[LEX ERROR] {e}")
        sys.exit(1)
    for lexeme, ttype in tokens:
        print(f"{lexeme!r:12} → {ttype}")

    # 4) Análisis sintáctico con recuperación de errores
    print("\n=== ANÁLISIS SINTÁCTICO ===")
    parser = Parser(grammar)
    try:
        ast, errors = parser.parse(tokens)
    except ParseError as e:
        print(f"[PARSE ERROR] {e}")
        sys.exit(1)

    if errors:
        print("\n--- ERRORES DE PARSEO ENCONTRADOS ---")
        for err in errors:
            print(err)
    else:
        print("Sin errores sintácticos.")

    # 5) Imprimir AST
    print("\n=== AST RESULTANTE ===")
    print(ast)


if __name__ == "__main__":
    main()
