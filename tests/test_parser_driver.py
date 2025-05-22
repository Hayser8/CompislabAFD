import pytest
from parser.parser_driver import Parser, ParseError
from parser.grammar import Grammar, Terminal, NonTerminal, Production

def make_simple_grammar():
    # Gramática: S → id
    S = NonTerminal("S")
    idt = Terminal("id")
    p0 = Production(0, S, (idt,))
    return Grammar({idt}, {S}, [p0], S)

# Caso válido: la entrada coincide con S → id
def test_parser_accepts_valid_input():
    grammar = make_simple_grammar()
    parser = Parser(grammar)
    tokens = [("foo", "id")]
    ast, errors = parser.parse(tokens)

    assert errors == []
    assert ast.name == "S"
    assert len(ast.children) == 1
    child = ast.children[0]
    assert child.name == "id"
    assert child.value == "id"

# Caso inválido: entrada vacía → debe fallar y devolver errores
def test_parser_rejects_invalid_input():
    grammar = make_simple_grammar()
    parser = Parser(grammar)
    ast, errors = parser.parse([])

    assert ast is None
    assert errors, "Debe reportar al menos un error"

# Entrada con token inesperado (ej. 'NUM' en lugar de 'id')
def test_parser_reports_unexpected_token():
    grammar = make_simple_grammar()
    parser = Parser(grammar)
    tokens = [("42", "NUM")]
    ast, errors = parser.parse(tokens)

    assert ast is None
    assert any("Unexpected token" in e for e in errors)
    assert any("NUM" in e for e in errors)

# Verifica que tras un error grave, el parser no construye AST
def test_parser_continues_after_panic():
    grammar = make_simple_grammar()
    parser = Parser(grammar)
    tokens = [("42", "NUM"), ("foo", "id")]
    ast, errors = parser.parse(tokens)

    assert ast is None
    assert len(errors) >= 1
    assert any("Unexpected token" in e for e in errors)
