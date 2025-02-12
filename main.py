from shunting_yard import shunting_yard
from arbolSINT import SyntaxTree
from DFA import DFA
if __name__ == "__main__":
    test_expressions = [ 
        "a|b.c*", 
        "(a|b)*.c", 
        "a.b|c*",  
        "a?(b|c)+",  
        "a.(b.c)*"
    ]

    for expr in test_expressions:
        try:
            ##Shunting
            postfix_expr = shunting_yard(expr)  
            ##Arbol 
            sint_tree = SyntaxTree(postfix_expr) 
            print("Nullable:", sint_tree.root.nullable)
            print("Firstpos:", {node.symbol.name for node in sint_tree.root.firstpos})
            print("Lastpos:", {node.symbol.name for node in sint_tree.root.lastpos})
            sint_tree.visualize(f"tree_{expr.replace('|', '_').replace('*', 'star').replace('(','P')}")  
            
            ## DFA
            dfa = DFA(sint_tree)
            dfa.visualize(f"tree_2{expr.replace('|', '_2').replace('*', 'star2')}")
            
            formatted_postfix = " ".join([s.name for s in postfix_expr]) 
            print(f"Infix: {expr}")
            print(f"Postfix: {formatted_postfix}\n")
        except ValueError as e:
            print(f"Infix: {expr}")
            print(f"❌ {e}\n")
