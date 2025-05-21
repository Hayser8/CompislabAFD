import pytest
from parser.parser_table import build_slr_table
from parser.parser_driver import Parser
from parser.grammar import Grammar, Terminal, NonTerminal, Production

def make_simple_grammar():
    # Gramática: program → stmt_list
    # stmt_list → stmt_list stmt | stmt
    # stmt → ID SEMICOLON
    S  = NonTerminal("program")
    SL = NonTerminal("stmt_list")
    ST = NonTerminal("stmt")
    ID = Terminal("ID")
    SC = Terminal("SEMICOLON")
    prods = [
        Production(0, S,  (SL,)),
        Production(1, SL, (SL, ST)),
        Production(2, SL, (ST,)),
        Production(3, ST, (ID, SC)),
    ]
    return Grammar(
        terminals={ID, SC},
        non_terminals={S, SL, ST},
        productions=prods,
        start_symbol=S
    )

def test_panic_mode_two_errors():
    G = make_simple_grammar()
    parser = Parser(G)
    # Ahora simulamos realmente un stmt sin ';' al final:
    #   "x y; y;"
    toks = [
        ("x", "ID"),    # falta ';' tras x
        ("y", "ID"), 
        (";", "SEMICOLON"),
        ("y", "ID"),
        (";", "SEMICOLON"),
    ]
    ast, errors = parser.parse(toks)
    # Debe haber al menos un error de parseo
    assert len(errors) >= 1
    assert "Unexpected token" in errors[0]
    # Y aún así haber construido un AST no-nulo gracias al segundo stmt
    assert ast is not None
