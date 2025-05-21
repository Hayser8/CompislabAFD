# tests/test_visualize_lr0.py

import sys, os
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.grammar import Grammar, Terminal, NonTerminal, Production
from parser.visualize_lr0 import lr0_to_dot

@pytest.fixture
def simple_grammar():
    # Gramática de prueba: S → a
    S = NonTerminal("S")
    a = Terminal("a")
    p = Production(0, S, (a,))
    return Grammar({a}, {S}, [p], S)

def test_lr0_dot_contains_states_and_edges(simple_grammar):
    dot = lr0_to_dot(simple_grammar)
    # Debe comenzar con 'digraph'
    assert dot.startswith("digraph LR0")
    # Debe tener al menos 3 nodos: 0,1,2
    assert re.search(r'node0 \[label="State 0:', dot)
    assert re.search(r'node1 \[label="State 1:', dot)
    assert re.search(r'node2 \[label="State 2:', dot)
    # Arista desde 0 a 1 con 'a'
    assert re.search(r'node0 -> node1 \[label="a"\];', dot)
    # Arista desde 0 a 2 con 'S'
    assert re.search(r'node0 -> node2 \[label="S"\];', dot)
