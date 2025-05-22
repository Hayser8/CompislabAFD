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
    # Simulamos un stmt sin ';' al final: "x y; y;"
    toks = [
        ("x", "ID"),    # falta ';' tras x
        ("y", "ID"),
        (";", "SEMICOLON"),
        ("y", "ID"),
        (";", "SEMICOLON"),
    ]
    ast, errors = parser.parse(toks)
    assert len(errors) >= 1
    assert "Unexpected token" in errors[0]
    assert ast is not None

def run_and_check(toks, expect_errors=True, expect_ast=True):
    """Función auxiliar para correr el parser y verificar errores y AST"""
    G = make_simple_grammar()
    parser = Parser(G)
    ast, errors = parser.parse(toks)
    print("Errores:", errors)
    print("AST:", ast)
    if expect_errors:
        assert len(errors) > 0
    else:
        assert len(errors) == 0
    if expect_ast:
        assert ast is not None
    else:
        assert ast is None

# -----------------------
# Tests individuales
# -----------------------

def test_valid_input():
    """Caso completamente válido, sin errores"""
    run_and_check([
        ("x", "ID"),
        (";", "SEMICOLON"),
        ("y", "ID"),
        (";", "SEMICOLON"),
    ], expect_errors=False)

def test_error_at_start():
    """Error al inicio, primer token inválido"""
    run_and_check([
        (";", "SEMICOLON"),
        ("x", "ID"),
        (";", "SEMICOLON"),
    ])

def test_error_at_end_without_sync():
    """Error al final, sin punto y coma ni token sincronizador"""
    run_and_check([
        ("x", "ID"),
        ("y", "ID"),
    ], expect_ast=False)

def test_sync_at_dollar():
    """Se sincroniza con '$' (fin de archivo)"""
    run_and_check([
        ("x", "ID"),
        ("y", "ID"),
        ("$", "$"),
    ], expect_ast=False)

def test_sync_with_rbrace():
    """Se sincroniza con '}' (RBRACE)"""
    run_and_check([
        ("x", "ID"),
        ("}", "RBRACE"),
        ("y", "ID"),
        (";", "SEMICOLON"),
    ])

def test_sync_with_rparen():
    """Se sincroniza con ')' (RPAREN)"""
    run_and_check([
        ("x", "ID"),
        (")", "RPAREN"),
        ("y", "ID"),
        (";", "SEMICOLON"),
    ])

def test_completely_invalid():
    """Entrada completamente inválida, sin tokens reconocibles"""
    run_and_check([
        ("?", "UNKNOWN"),
        ("@", "UNKNOWN"),
        ("$", "$"),
    ], expect_ast=False)
