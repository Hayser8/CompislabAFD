from shunting_yard import shunting_yard
from symbol import Symbol  

if __name__ == "__main__":
    test_expressions = [
        "a|b.c*", 
        "(a|b)*.c", 
        "a.b|c*",  
        "a?(b|c)+",  
        "a.(b.c)*"  
    ]

    for expr in test_expressions:
        postfix_expr = shunting_yard(expr)  
        formatted_postfix = " ".join([s.name for s in postfix_expr])  
        print(f"Infix: {expr}")
        print(f"Postfix: {formatted_postfix}\n")
