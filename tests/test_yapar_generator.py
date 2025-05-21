# tests/test_yapar_generator.py

import sys, os
import importlib.util
import textwrap
import pytest

# Añadir tmpdir al path para imports dinámicos
from pathlib import Path

def _import_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_generator_creates_working_parser(tmp_path, monkeypatch):
    # 1) Creamos .yalp
    yalp = tmp_path / "grammar.yalp"
    yalp.write_text(textwrap.dedent("""
        %token ID
        %%
        S : ID ;
    """))

    # 2) Creamos módulo lexeitor.py con scan mínimo
    lexer = tmp_path / "lexeitor.py"
    lexer.write_text(textwrap.dedent("""
        def scan(text):
            # Devuelve [(lexeme, type)], simulando el lexer
            return [(text.strip(), text.strip())]
    """))

    # 3) Inyectamos cwd al path
    sys.path.insert(0, str(tmp_path))

    # 4) Generamos parser_gen.py
    from yapar_generator import generate_parser_code
    out = tmp_path / "parser_gen.py"
    generate_parser_code(str(yalp), "lexeitor", str(out))

    # 5) Importamos el parser generado
    parser_mod = _import_mod(out, "parser_gen")
    assert hasattr(parser_mod, "parse")
    assert hasattr(parser_mod, "grammar")
    assert hasattr(parser_mod, "ACTION")
    assert hasattr(parser_mod, "GOTO")

    # 6) Probamos parse() con input válido
    assert parser_mod.parse("ID") is True

    # 7) Y con input inválido (otro token) debe lanzar
    with pytest.raises(Exception):
        parser_mod.parse("WRONG")
