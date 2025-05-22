# tests/test_first_follow.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.grammar import Grammar, Terminal, NonTerminal, Production, EPSILON
from parser.first_follow import FirstFollowCalculator

@pytest.fixture
def simple_grammar():
    # Gramática: S → A a | ε ; A → b
    S = NonTerminal("S")
    A = NonTerminal("A")
    a = Terminal("a")
    b = Terminal("b")
    prods = [
        Production(0, S, (A, a)),
        Production(1, S, (EPSILON,)),
        Production(2, A, (b,))
    ]
    return Grammar(
        terminals={a, b},
        non_terminals={S, A},
        productions=prods,
        start_symbol=S
    )

# Verifica FIRST(A), FIRST(S), FIRST(a)
def test_first_sets(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    assert ffc.get_first(NonTerminal("A")) == {Terminal("b")}
    assert ffc.get_first(NonTerminal("S")) == {Terminal("b"), EPSILON}
    assert ffc.get_first(Terminal("a")) == {Terminal("a")}

# Verifica FOLLOW(S) = {$} y FOLLOW(A) = {a}
def test_follow_sets(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    S, A = NonTerminal("S"), NonTerminal("A")
    assert Terminal("$") in ffc.get_follow(S)
    assert Terminal("a") in ffc.get_follow(A)

# Verifica que el FIRST de una secuencia vacía sea ε
def test_first_of_empty_sequence(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    assert ffc._first_of_sequence([]) == {EPSILON}

# Verifica identidad de EPSILON
def test_epsilon_singleton(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    assert ffc.EPSILON is EPSILON

# FIRST con símbolo que deriva ε indirectamente
def test_first_with_indirect_epsilon():
    S, A, B = NonTerminal("S"), NonTerminal("A"), NonTerminal("B")
    b = Terminal("b")
    prods = [
        Production(0, S, (A, B)),
        Production(1, A, (EPSILON,)),
        Production(2, B, (b,))
    ]
    G = Grammar(
        terminals={b},
        non_terminals={S, A, B},
        productions=prods,
        start_symbol=S
    )
    ffc = FirstFollowCalculator(G)
    assert ffc.get_first(S) == {b}
    assert ffc.get_first(A) == {EPSILON}
    assert ffc.get_first(B) == {b}

# FOLLOW desde diferentes contextos de aparición
def test_follow_with_multiple_contexts():
    S, A, B, C = NonTerminal("S"), NonTerminal("A"), NonTerminal("B"), NonTerminal("C")
    a, b, c = Terminal("a"), Terminal("b"), Terminal("c")
    prods = [
        Production(0, S, (A, B, C)),
        Production(1, A, (a,)),
        Production(2, A, (EPSILON,)),
        Production(3, B, (b,)),
        Production(4, C, (c,))
    ]
    G = Grammar(
        terminals={a, b, c},
        non_terminals={S, A, B, C},
        productions=prods,
        start_symbol=S
    )
    ffc = FirstFollowCalculator(G)
    assert b in ffc.get_follow(A)
    assert c in ffc.get_follow(B)
    assert Terminal('$') in ffc.get_follow(C)

# Cadena completa anulable: A → ε, B → ε, FIRST(S) = FIRST(C)
def test_first_with_full_nullable_chain():
    S, A, B, C = NonTerminal("S"), NonTerminal("A"), NonTerminal("B"), NonTerminal("C")
    c = Terminal("c")
    prods = [
        Production(0, S, (A, B, C)),
        Production(1, A, (EPSILON,)),
        Production(2, B, (EPSILON,)),
        Production(3, C, (c,))
    ]
    G = Grammar(
        terminals={c},
        non_terminals={S, A, B, C},
        productions=prods,
        start_symbol=S
    )
    ffc = FirstFollowCalculator(G)
    assert ffc.get_first(S) == {c}
    assert ffc.get_first(A) == {EPSILON}
    assert ffc.get_first(B) == {EPSILON}
    assert ffc.get_first(C) == {c}
