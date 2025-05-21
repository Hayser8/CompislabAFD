# tests/test_grammar.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.grammar import Terminal, NonTerminal, Production, Grammar

@pytest.fixture
def simple_grammar():
    a, b = Terminal("a"), Terminal("b")
    S, A = NonTerminal("S"), NonTerminal("A")
    p1 = Production(0, head=S, body=(a, A))
    p2 = Production(1, head=S, body=(b,))
    return Grammar(
        terminals={a, b},
        non_terminals={S, A},
        productions=[p1, p2],
        start_symbol=S
    )

def test_production_head_type(simple_grammar):
    for p in simple_grammar.productions:
        assert isinstance(p.head, NonTerminal)

def test_production_repr(simple_grammar):
    assert repr(simple_grammar.productions[0]) == "S → a A"

def test_grammar_repr_includes_sections(simple_grammar):
    rep = repr(simple_grammar)
    assert "Terminals:" in rep
    assert "NonTerminals:" in rep
    assert "Start Symbol: S" in rep
    assert "S → a A" in rep and "S → b" in rep

def test_augmented_grammar(simple_grammar):
    G2 = simple_grammar.augmented()
    assert G2.start_symbol.name.endswith("'")
    prod0 = G2.productions[0]
    assert prod0.head == G2.start_symbol
    assert prod0.body == (simple_grammar.start_symbol,)

def test_immutable_collections(simple_grammar):
    tset = simple_grammar.terminals
    tset.add(Terminal("c"))
    assert Terminal("c") not in simple_grammar.terminals
