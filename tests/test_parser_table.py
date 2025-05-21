# tests/test_parser_table.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.grammar import Grammar, Terminal, NonTerminal, Production
from parser.parser_table import build_slr_table

def test_slr_table_simple():
    # Gramática mínima: S → id
    S  = NonTerminal("S")
    idt = Terminal("id")
    p0 = Production(0, S, (idt,))
    g  = Grammar({idt}, {S}, [p0], S)

    action, goto = build_slr_table(g)

    # Estado 0: on 'id' shift a estado 1
    assert action[(0, idt)] == ('s', 1)
    # GOTO[0, S] == 2
    assert goto[(0, S)] == 2

    dollar = Terminal('$')
    # Estado 1: reduce por p0 en '$'
    assert action[(1, dollar)] == ('r', 0)
    # Estado 2: accept en '$'
    assert action[(2, dollar)] == ('acc', 0)
