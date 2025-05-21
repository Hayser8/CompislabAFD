import pytest
from parser.parser_driver import Parser, ParseError
from parser.grammar       import Grammar, Terminal, NonTerminal, Production

def make_simple_grammar():
    # Gramática trivial: S → id
    S = NonTerminal("S")
    idt = Terminal("id")
    p0 = Production(0, S, (idt,))
    return Grammar({idt}, {S}, [p0], S)

def test_parser_accepts_valid_input():
    grammar = make_simple_grammar()
    parser = Parser(grammar)
    tokens = [("foo", "id")]
    result = parser.parse(tokens)
    # ahora parse devuelve (ast, errors)
    ast, errors = result
    # no debe haber errores
    assert errors == []
    # y el AST raíz debe ser un nodo S
    # (en tu implementación por defecto hace un ASTNode("S", None, [ASTNode("id", "id")]))
    assert ast.name == "S"
    assert len(ast.children) == 1
    child = ast.children[0]
    assert child.name == "id"
    assert child.value == "id"

def test_parser_rejects_invalid_input():
    grammar = make_simple_grammar()
    parser = Parser(grammar)
    # sin tokens -> error de fin de entrada
    ast, errors = parser.parse([])
    assert ast is None
    assert errors, "Debe reportar al menos un error"
