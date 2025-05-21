import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from parser.yalp_lexer import Tok, remove_comments, tokenize

def test_remove_comments_simple():
    text = "code /* comment */ more"
    cleaned = remove_comments(text)
    assert cleaned == ["code               more"]

def test_remove_comments_multiline_across_lines():
    text = "a /* line1\nline2 */ b"
    cleaned = remove_comments(text)
    # primera línea pierde el comentario
    assert cleaned[0].startswith("a  ")
    # segunda línea mantiene ' b' al final
    assert cleaned[1].endswith("  b")

def test_tokenize_basic_directives():
    text = (
        "%token ID NUM\n"
        "IGNORE WS\n"
        "%%\n"
        "S : ID ;"
    )
    toks = list(tokenize(text))
    result = [(t.type, t.lexeme, t.line, t.column) for t in toks]
    assert result == [
        ("PERCENT_TOKEN", "%token", 1, 1),
        ("IDENTIFIER",   "ID",     1, 8),
        ("IDENTIFIER",   "NUM",    1, 11),
        ("IGNORE",       "IGNORE", 2, 1),
        ("IDENTIFIER",   "WS",     2, 8),
        ("PERCENT_PERCENT", "%%",  3, 1),
        ("IDENTIFIER",   "S",      4, 1),
        (":",            ":",      4, 3),
        ("IDENTIFIER",   "ID",     4, 5),
        (";",            ";",      4, 8),
    ]

def test_tokenize_with_comments_ignored():
    text = (
        "/* intro */\n"
        "%token A /* inline */ B\n"
        "X|Y; IGNORE Z\n"
        "%%"
    )
    toks = list(tokenize(text))
    result = [(t.type, t.lexeme) for t in toks]
    expected = [
        ("PERCENT_TOKEN", "%token"),  # lexeme correctamente "%token"
        ("IDENTIFIER",    "A"),
        ("IDENTIFIER",    "B"),
        ("IDENTIFIER",    "X"),
        ("|",             "|"),
        ("IDENTIFIER",    "Y"),
        (";",             ";"),
        ("IGNORE",        "IGNORE"),
        ("IDENTIFIER",    "Z"),
        ("PERCENT_PERCENT", "%%"),
    ]
    assert result == expected

def test_tokenize_error_on_bad_character():
    with pytest.raises(SyntaxError):
        list(tokenize("S $ ;"))
