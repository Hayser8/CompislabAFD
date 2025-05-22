import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.grammar import Grammar, Terminal, NonTerminal, Production
from parser.parser_table import build_slr_table

# Gramática básica: S → id
def test_slr_table_simple():
    S  = NonTerminal("S")
    idt = Terminal("id")
    p0 = Production(0, S, (idt,))
    g  = Grammar({idt}, {S}, [p0], S)

    action, goto = build_slr_table(g)
    dollar = Terminal('$')

    assert action[(0, idt)] == ('s', 1)
    assert goto[(0, S)] == 2
    assert action[(1, dollar)] == ('r', 0)
    assert action[(2, dollar)] == ('acc', 0)

# Gramática con múltiples FOLLOW: S → A ; A → a | b
def test_slr_table_with_follow_set():
    S, A = NonTerminal("S"), NonTerminal("A")
    a, b = Terminal("a"), Terminal("b")
    p0 = Production(0, S, (A,))
    p1 = Production(1, A, (a,))
    p2 = Production(2, A, (b,))
    g = Grammar({a, b}, {S, A}, [p0, p1, p2], S)

    action, goto = build_slr_table(g)

    # Estado 0 debería tener shift en 'a' y 'b'
    assert ('s', 1) == action.get((0, a)) or action.get((0, b))  # alguno debe ser shift

    # Debe haber una reducción por p1 en FOLLOW(A)
    reduce_actions = [(k, v) for k, v in action.items() if v[0] == 'r']
    assert any(v == ('r', 1) for _, v in reduce_actions)
    assert any(v == ('r', 2) for _, v in reduce_actions)

# Gramática en la que S → A B ; A → a ; B → b
def test_slr_table_goto_multiple_symbols():
    S, A, B = NonTerminal("S"), NonTerminal("A"), NonTerminal("B")
    a, b = Terminal("a"), Terminal("b")
    p0 = Production(0, S, (A, B))
    p1 = Production(1, A, (a,))
    p2 = Production(2, B, (b,))
    g = Grammar({a, b}, {S, A, B}, [p0, p1, p2], S)

    action, goto = build_slr_table(g)

    assert (0, A) in goto
    assert (0, B) not in goto  # B no aparece aún

    # GOTO después de procesar A debe incluir transición a estado con B
    for (state_id, sym), target in goto.items():
        if sym == A:
            next_state = target
            assert (next_state, B) in goto

# Producción aumentada debe aceptar en el estado final
def test_augmented_accept():
    S = NonTerminal("S")
    x = Terminal("x")
    p0 = Production(0, S, (x,))
    g = Grammar({x}, {S}, [p0], S)

    action, goto = build_slr_table(g)
    accept_states = [(k, v) for k, v in action.items() if v[0] == 'acc']
    assert any(term.name == '$' for (state, term), _ in accept_states)
