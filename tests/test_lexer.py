# test_lexer.py
import pytest
from lexer.lexeitor import scan, LexerError

# Helper para extraer sólo los tipos de token de la salida de scan()
def token_types(src):
    return [tok for (_, tok) in scan(src)]

@pytest.mark.parametrize("src, expected", [
    # Identificadores y palabras clave
    ("foo bar\n", ["IDENTIFIER", "IDENTIFIER", "NEWLINE", "DEDENT"]),
    ("if x else\n", ["IF", "IDENTIFIER", "ELSE", "NEWLINE", "DEDENT"]),
    # Números enteros y flotantes
    ("123 0b1010 3.14 .5 2e10\n",
     ["INTEGER","INTEGER","FLOAT","FLOAT","FLOAT","NEWLINE","DEDENT"]),
    # Strings simples y triples
    ("'a' \"b\"\n", ["STRING","STRING","NEWLINE","DEDENT"]),
    ("'''multi\nline''' \"\"\"other\"\"\"\n",
     ["STRING","STRING","NEWLINE","DEDENT"]),
    # Operadores y delimitadores
    ("a + b - c * d / e % f == != <= >= : , ; . -> ** // += -= *= /= %=\n",
     ["IDENTIFIER","PLUS","IDENTIFIER","MINUS","IDENTIFIER","TIMES","IDENTIFIER",
      "DIV","IDENTIFIER","MODULO","IDENTIFIER","EQ","NE","LE","GE","COLON",
      "COMMA","SEMICOLON","DOT","RARROW","POW","FLOORDIV",
      "PLUSEQ","MINEQ","TIMEQ","DIVEQ","MODEQ","NEWLINE","DEDENT"]),
    # Paréntesis, corchetes, llaves
    ("( ) [ ] { }\n",
     ["LPAREN","RPAREN","LBRACKET","RBRACKET","LBRACE","RBRACE","NEWLINE","DEDENT"]),
    # Comentarios y whitespace
    ("x = 1  # esto es un comment\n y=2\n",
     ["IDENTIFIER","ASSIGN","INTEGER","NEWLINE","IDENTIFIER","ASSIGN","INTEGER","NEWLINE","DEDENT"]),
    # Indentación y dedentación
    ("def f():\n"
     "    x = 1\n"
     "    if x:\n"
     "        y = 2\n"
     "    z = 3\n",
     ["DEF","IDENTIFIER","LPAREN","RPAREN","COLON","NEWLINE",
      "INDENT",
        "IDENTIFIER","ASSIGN","INTEGER","NEWLINE",
        "IF","IDENTIFIER","COLON","NEWLINE",
        "INDENT",
          "IDENTIFIER","ASSIGN","INTEGER","NEWLINE",
        "DEDENT",
        "IDENTIFIER","ASSIGN","INTEGER","NEWLINE",
      "DEDENT",
      "DEDENT"]),
])
def test_scan_various(src, expected):
    assert token_types(src) == expected

def test_unclosed_string_raises():
    with pytest.raises(LexerError):
        scan("'unclosed string\n")

def test_invalid_symbol_raises():
    with pytest.raises(LexerError):
        scan("@@@@@\n")

def test_multiple_dedents():
    # Al final siempre sale el DEDENT al nivel 0
    toks = token_types("a\n")
    assert toks[-1] == "DEDENT"
