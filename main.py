from shunting_yard import shunting_yard

if __name__ == "__main__":
    test_expressions = [
        "a|b.c*", 
        "(a|b)*.c", 
        "a.b|c*",  
        "a?(b|c)+",  
        "a.(b.c)*",  
        "(a|b.c",  
        "a|b)#c",  
        "a||b.c"  
    ]

    for expr in test_expressions:
        try:
            postfix_expr = shunting_yard(expr)  
            formatted_postfix = " ".join([s.name for s in postfix_expr])  
            print(f"Infix: {expr}")
            print(f"Postfix: {formatted_postfix}\n")
        except ValueError as e:
            print(f"Infix: {expr}")
            print(f"❌ {e}\n")
