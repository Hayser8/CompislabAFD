import textwrap
import pytest
from parser.yapar_parser import YalpParser
from parser.yalp_lexer   import tokenize
from parser.grammar      import Grammar, Terminal, NonTerminal

def test_yalp_parser_simple_grammar():
    spec = textwrap.dedent("""
        %token A B
        IGNORE WS
        %%
        S : A B ;
    """).strip()
    toks = list(tokenize(spec))
    assert toks, "La lista de tokens no debe estar vacía"

    parser = YalpParser(toks)
    grammar = parser.parse()

    # 1) tipo
    assert isinstance(grammar, Grammar)
    # 2) start_symbol debe ser NonTerminal("S")
    assert grammar.start_symbol == NonTerminal("S")
    # 3) terminales
    expected_terms = {Terminal("A"), Terminal("B"), Terminal("WS")}
    assert grammar.terminals == expected_terms
    # 4) no-terminales
    assert grammar.non_terminals == {NonTerminal("S")}
    # 5) producciones: exactamente una
    prods = grammar.productions
    assert len(prods) == 1
    prod = prods[0]
    # ahora prod.head es NonTerminal, no str
    assert prod.head == NonTerminal("S")
    # cuerpo correcto
    assert tuple(prod.body) == (Terminal("A"), Terminal("B"))
