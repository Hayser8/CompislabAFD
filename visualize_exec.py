#!/usr/bin/env python3
# visualize_executor.py
"""
Módulo ejecutor para generar lr0.pdf desde la gramática YAPar.
"""

import sys
import os
import argparse

def main():
    p = argparse.ArgumentParser(
        description="Genera el autómata LR(0) en PDF desde una .yalp"
    )
    p.add_argument("grammar_yalp", help="Archivo .yalp con la gramática YAPar")
    args = p.parse_args()

    sys.path.insert(0, os.getcwd())

    from parser.yalp_lexer   import tokenize as yalp_tokenize
    from parser.yalp_parser  import YalpParser
    from parser.visualize_lr0 import visualize_lr0

    # 1) Cargar y parsear gramática
    try:
        yalp_txt = open(args.grammar_yalp, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"[ERROR] No existe '{args.grammar_yalp}'")
        sys.exit(1)

    yalp_toks = list(yalp_tokenize(yalp_txt))
    try:
        grammar = YalpParser(yalp_toks).parse()
    except Exception as e:
        print(f"[ERROR] Falló parsing de gramática: {e}")
        sys.exit(1)

    # 2) Generar LR(0) en PDF
    try:
        print("=== Generando autómata LR(0) en PDF ===")
        visualize_lr0(grammar, filename="lr0", format="pdf")
        print("=== Autómata guardado en 'lr0.pdf' ===")
    except Exception as e:
        print(f"[ERROR] Falló visualización: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
