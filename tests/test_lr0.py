# tests/test_canonical.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.grammar import Grammar, Terminal, NonTerminal, Production
from parser.lr0 import Item, State, closure, goto, build_canonical

@pytest.fixture
def small_grammar():
    # S → A
    # A → a
    S = NonTerminal("S")
    A = NonTerminal("A")
    a = Terminal("a")
    p1 = Production(0, S, (A,))
    p2 = Production(1, A, (a,))
    return Grammar(
        terminals={a},
        non_terminals={S, A},
        productions=[p1, p2],
        start_symbol=S
    )

def test_item_and_advance_dot():
    S = NonTerminal("S")
    a = Terminal("a")
    prod = Production(0, S, (a, a))
    itm = Item(prod, 0)
    assert itm.next_symbol() == a
    itm2 = itm.advance_dot()
    assert itm2.dot == 1 and itm2.production == prod
    with pytest.raises(ValueError):
        Item(prod, 2).advance_dot()

def test_closure_adds_items(small_grammar):
    G = small_grammar
    p1, p2 = G.productions
    clos = closure(G, {Item(p1, 0)})  # S → ·A
    assert Item(p1, 0) in clos
    assert Item(p2, 0) in clos  # añade A → ·a

def test_goto_shifts_and_closes(small_grammar):
    G = small_grammar
    p1, _ = G.productions
    ini = closure(G, {Item(p1, 0)})
    st = goto(G, ini, NonTerminal("A"))
    assert st == {Item(p1, 1)}

def test_build_canonical_counts_states(small_grammar):
    G = small_grammar
    states = build_canonical(G)
    # Con S'→S, S→A, A→a tendremos 4 estados:
    #   0: ·S', ·S, ·A, ·a
    #   1: S'·
    #   2: A··  
    #   3: a··
    assert len(states) == 4

def test_state_repr_contains_all_dots(small_grammar):
    states = build_canonical(small_grammar)
    rep0 = repr(states[0])
    # Debe listar cierres para S'→· S, S→· A y A→· a
    assert "· S" in rep0
    assert "· A" in rep0
    assert "· a" in rep0
