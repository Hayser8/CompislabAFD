import graphviz
from typing import List
from parser.lr0 import State, build_canonical, goto, Item
from parser.grammar import Grammar, NonTerminal

def visualize_lr0(grammar: Grammar,
                  filename: str = "lr0",
                  format: str = "pdf") -> None:
    """
    Construye y renderiza el autómata LR(0) de la gramática usando graphviz
    de forma legible y con una sola augmentación.
    """
    # ————————————————————————————————
    # 1) Augment idempotente
    if grammar.start_symbol.name.endswith("'"):
        aug = grammar
    else:
        aug = grammar.augmented()

    # 2) Colección canónica LR(0)
    states: List[State] = build_canonical(aug)

    # ————————————————————————————————
    # 3) Configurar Digraph
    dot = graphviz.Digraph("LR0",
                           filename=filename,
                           format=format)
    dot.attr(rankdir="LR",
             splines="ortho",
             nodesep="0.4",
             ranksep="0.3")
    dot.attr("node",
             shape="record",
             fontname="Courier",
             fontsize="10",
             height="0.2")

    # ————————————————————————————————
    # 4) Añadir nodos con kernel‐items
    for st in states:
        # kernel = items con punto != 0, más siempre el ítem inicial
        kernel_items = []
        for itm in st.items:
            # itm is an Item; asumimos .production y .dot propiedades
            if itm.production.head == aug.start_symbol or itm.dot > 0:
                kernel_items.append(itm)
        # render en record: {ID | item1\l item2\l ...}
        lines = [repr(itm) for itm in kernel_items]
        # Graphviz record usa '\l' para salto y alineación a la izquierda
        label = "{" + str(st.id) + " | " + "\\l".join(lines) + "\\l}"
        dot.node(str(st.id), label=label)

    # ————————————————————————————————
    # 5) Añadir aristas (shift/goto)
    for st in states:
        symbols = {itm.next_symbol() for itm in st.items if itm.next_symbol() is not None}
        ordered = sorted(symbols, key=lambda s: (isinstance(s, NonTerminal), str(s)))
        for sym in ordered:
            tgt_items = goto(aug, st.items, sym)
            if not tgt_items:
                continue
            tgt_state = next(s for s in states if s.items == tgt_items)
            dot.edge(str(st.id), str(tgt_state.id), label=str(sym))

    # ————————————————————————————————
    # 6) Renderizar y borrar intermedios
    dot.render(cleanup=True)
