#!/usr/bin/env python3
import argparse
import sys
from collections import defaultdict
from parser.yalp_lexer    import tokenize as yalp_tokenize
from parser.yalp_parser   import YalpParser
from parser.first_follow  import FirstFollowCalculator
from parser.lr0           import build_canonical, goto, Item, State
from parser.parser_table  import build_slr_table
from parser.parser_driver import Parser, ParseError
from parser.grammar       import Grammar, Terminal, NonTerminal

def print_first_follow(grammar: Grammar):
    print("=== FIRST sets ===")
    ff = FirstFollowCalculator(grammar)
    for nt in sorted(grammar.non_terminals, key=lambda x: x.name):
        first = sorted(ff.get_first(nt), key=lambda t: t.name)
        print(f"FIRST({nt}) = {{{', '.join(map(str, first))}}}")
    print("\n=== FOLLOW sets ===")
    for nt in sorted(grammar.non_terminals, key=lambda x: x.name):
        follow = sorted(ff.get_follow(nt), key=lambda t: t.name)
        print(f"FOLLOW({nt}) = {{{', '.join(map(str, follow))}}}")

def print_lr0_states(grammar: Grammar):
    print("\n=== LR(0) canonical collection ===")
    aug = grammar.augmented()
    states = build_canonical(aug)
    for st in states:
        print(st)
        print("-" * 40)

def debug_slr_conflicts(grammar: Grammar):
    """
    Recrea build_slr_table pero capturando conflictos:
    - shift/reduce
    - reduce/reduce
    """
    aug = grammar.augmented()
    states = build_canonical(aug)
    ff = FirstFollowCalculator(grammar)

    action: Dict[(int, Terminal), Tuple[str,int]] = {}
    conflicts: List[str] = []

    for st in states:
        for itm in st.items:
            a = itm.next_symbol()
            # SHIFT cases
            if isinstance(a, Terminal):
                j_items = goto(aug, set(st.items), a)
                if j_items:
                    j = next(s.id for s in states if s.items == j_items)
                    key = (st.id, a)
                    new = ('s', j)
                    if key in action and action[key] != new:
                        conflicts.append(
                            f"Shift/Shift conflict in state {st.id} on '{a}': {action[key]} vs {new}"
                        )
                    action[key] = new
            # REDUCE/ACCEPT
            elif a is None:
                prod = itm.production
                if prod.id < 0:
                    key = (st.id, Terminal('$'))
                    new = ('acc', 0)
                    if key in action and action[key] != new:
                        conflicts.append(
                            f"Accept conflict in state {st.id}"
                        )
                    action[key] = new
                else:
                    for b in ff.get_follow(prod.head):
                        key = (st.id, b)
                        new = ('r', prod.id)
                        if key in action:
                            prev = action[key]
                            if prev[0] == 's':
                                conflicts.append(
                                    f"Shift/Reduce conflict in state {st.id} on '{b}': shift to {prev[1]} vs reduce by prod {prod}"
                                )
                            elif prev[0] == 'r' and prev[1] != prod.id:
                                conflicts.append(
                                    f"Reduce/Reduce conflict in state {st.id} on '{b}': reduce by {prev[1]} vs {prod.id}"
                                )
                        action[key] = new

    print("\n=== SLR(1) conflicts ===")
    if not conflicts:
        print("No conflicts found. Tu gramática es SLR(1).")
    else:
        for c in conflicts:
            print(c)

def debug_parse_source(grammar: Grammar, source_file: str):
    print(f"\n=== Parseando fuente: {source_file} ===")
    with open(source_file, encoding="utf-8") as f:
        src = f.read()
    # normalizar finales
    src = src.replace("\r\n", "\n").replace("\r", "\n")
    from parser.yalp_lexer import tokenize as yalp_lex
    tokens = list(yalp_lex(src))
    parser = Parser(grammar)
    try:
        ast, errors = parser.parse(tokens)
        if errors:
            print("** Errores detectados por el parser **")
            for e in errors:
                print(e)
        else:
            print("Parseo OK. AST:")
            print(ast)
    except ParseError as e:
        print("ParseError (no recuperable):", e)

def main():
    ap = argparse.ArgumentParser(description="Debug de gramática YAPar")
    ap.add_argument("grammar", help="Fichero .yalp")
    ap.add_argument("--source", "-s", help="Fichero fuente a parsear", default=None)
    args = ap.parse_args()

    # 1) Carga y parse de la gramática YAPar
    text = open(args.grammar, encoding="utf-8").read()
    toks = list(yalp_tokenize(text))
    try:
        grammar = YalpParser(toks).parse()
    except Exception as e:
        print("Error parseando la gramática:", e)
        sys.exit(1)

    # 2) FIRST/FOLLOW
    print_first_follow(grammar)

    # 3) LR(0) states
    print_lr0_states(grammar)

    # 4) SLR conflicts
    debug_slr_conflicts(grammar)

    # 5) (opcional) parsear un archivo de prueba
    if args.source:
        debug_parse_source(grammar, args.source)

if __name__ == "__main__":
    main()
