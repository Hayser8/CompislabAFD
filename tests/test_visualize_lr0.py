import sys, os
import re
import pytest
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parser.grammar import Grammar, Terminal, NonTerminal, Production
from parser.visualize_lr0 import visualize_lr0

@pytest.fixture
def simple_grammar():
    # Gramática: S → a
    S = NonTerminal("S")
    a = Terminal("a")
    p = Production(0, S, (a,))
    return Grammar({a}, {S}, [p], S)

def test_visualize_creates_pdf(tmp_path, simple_grammar):
    filename = tmp_path / "test_lr0"
    visualize_lr0(simple_grammar, filename=str(filename), format="pdf")

    # Esperamos que Graphviz haya generado un .pdf y eliminado archivos intermedios
    pdf_file = str(filename) + ".pdf"
    assert os.path.exists(pdf_file)
    assert os.path.getsize(pdf_file) > 0

def test_visualize_respects_augmented_symbol(tmp_path):
    # Gramática ya aumentada (S')
    S_prime = NonTerminal("S'")
    S = NonTerminal("S")
    a = Terminal("a")
    prods = [
        Production(-1, S_prime, (S,)),
        Production(0, S, (a,))
    ]
    g = Grammar({a}, {S, S_prime}, prods, S_prime)

    filename = tmp_path / "test_aug"
    visualize_lr0(g, filename=str(filename), format="pdf")

    assert os.path.exists(str(filename) + ".pdf")
