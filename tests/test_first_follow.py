# tests/test_first_follow.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.grammar import Grammar, Terminal, NonTerminal, Production, EPSILON
from parser.first_follow import FirstFollowCalculator

@pytest.fixture
def simple_grammar():
    # Gramática de prueba:
    #   S → A a | ε
    #   A → b
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

def test_first_sets(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    # FIRST(A) = {b}
    assert ffc.get_first(NonTerminal("A")) == {Terminal("b")}
    # FIRST(S) = {b, ε}  ← aquí no entra 'a' porque A no genera ε
    assert ffc.get_first(NonTerminal("S")) == {Terminal("b"), EPSILON}
    # FIRST(a) = {a}
    assert ffc.get_first(Terminal("a")) == {Terminal("a")}

def test_follow_sets(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    S, A = NonTerminal("S"), NonTerminal("A")
    assert Terminal("$") in ffc.get_follow(S)
    assert Terminal("a") in ffc.get_follow(A)

def test_first_of_empty_sequence(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    assert ffc._first_of_sequence([]) == {EPSILON}

def test_epsilon_singleton(simple_grammar):
    ffc = FirstFollowCalculator(simple_grammar)
    assert ffc.EPSILON is EPSILON
