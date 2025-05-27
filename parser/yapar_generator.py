import os
from typing import Set, List
from parser.yalp_lexer import tokenize
from parser.yalp_parser import YalpParser
from parser.parser_table import build_slr_table
from parser.grammar import Grammar, Terminal, NonTerminal, Production
import textwrap

def _repr_set_ob(self_set: Set, tpl_name: str) -> str:
    """
    Devuelve un literal Python de un set de objetos con __repr__ amigable.
    p.ej. {Terminal("A"), ...} -> '{Terminal("A"), ...}'
    """
    items = ", ".join(repr(x) for x in sorted(self_set, key=lambda x: repr(x)))
    return f"{{{items}}}"

def _repr_list_ob(self_list: List, tpl_name: str) -> str:
    """
    Devuelve un literal Python de una lista de Production.
    """
    lines = []
    for p in self_list:
        lines.append(f"    {repr(p)}")
    return "[\n" + ",\n".join(lines) + "\n]"

def generate_parser_code(
    yalp_file: str,
    lexer_module: str,
    out_file: str = "parser_gen.py"
):
    """
    Genera un módulo Python con el parser SLR(1).

    :param yalp_file: ruta al .yalp con la gramática.
    :param lexer_module: nombre del módulo Python del lexer (p.ej. 'lexeitor').
    :param out_file: ruta del fichero de salida.
    """
    # 1) Parsear el .yalp a Grammar
    text = open(yalp_file, encoding="utf-8").read()
    toks = list(tokenize(text))
    grammar: Grammar = YalpParser(toks).parse()

    # 2) Construir tablas SLR(1)
    action, goto = build_slr_table(grammar)

    # 3) Serializar Grammar y tablas
    terms_repr = _repr_set_ob(grammar.terminals, "Terminal")
    nonterms_repr = _repr_set_ob(grammar.non_terminals, "NonTerminal")
    prods_repr = _repr_list_ob(grammar.productions, "Production")
    start_repr = repr(grammar.start_symbol)

    # ACTION y GOTO como literales sencillos
    action_lines = ["ACTION = {"]
    for (st, t), (kind, val) in sorted(action.items(), key=lambda kv: (kv[0][0], repr(kv[0][1]))):
        action_lines.append(f"    ({st}, {repr(t)}) : ({repr(kind)}, {val}),")
    action_lines.append("}\n")

    goto_lines = ["GOTO = {"]
    for (st, nt), target in sorted(goto.items(), key=lambda kv: (kv[0][0], repr(kv[0][1]))):
        goto_lines.append(f"    ({st}, {repr(nt)}) : {target},")
    goto_lines.append("}\n")

    # 4) Template del módulo
    tpl = f"""
# Autogenerado por Yapar – no editar manualmente

from {lexer_module} import scan
from parser_driver import Parser, ParseError
from grammar import Grammar, Terminal, NonTerminal, Production

# Gramática
grammar = Grammar(
    terminals={terms_repr},
    non_terminals={nonterms_repr},
    productions={prods_repr},
    start_symbol={start_repr}
)

# Tablas SLR(1)
{textwrap.indent(chr(10).join(action_lines), '""')}
{textwrap.indent(chr(10).join(goto_lines), '""')}

# Construimos el parser
parser = Parser(grammar)

def parse(text: str) -> bool:
    \"\"\"
    Tokeniza `text` con el lexer y ejecuta el análisis sintáctico.
    \"\"\"
    tokens = scan(text)
    return parser.parse(tokens)
"""

    # 5) Guardar el fichero
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(tpl).strip() + "\n")
    print(f"✔ Parser generado en «{out_file}»")
