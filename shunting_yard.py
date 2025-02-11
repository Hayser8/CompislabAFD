from symbol import Symbol  # Importamos la clase Symbol

# Precedencia de los operadores (Mayor número = mayor precedencia)
precedence = {
    '|': 1,  # Unión
    '.': 2,  # Concatenación (implícita)
    '*': 3,  # Cerradura de Kleene
    '+': 3,  
    '?': 3   
}

# Asociación de operadores (Izquierda o derecha)
associativity = {
    '|': "left",
    '.': "left",
    '*': "right",
    '+': "right",
    '?': "right"
}


def shunting_yard(expression):
    """
    Convierte una expresión regular en notación infix a postfix usando el algoritmo de Shunting Yard.
    """
    output_queue = []  # Cola de salida (postfix)
    operator_stack = []  # Pila de operadores

    for char in expression:
        if char.isalnum():  # Si es un símbolo, lo agregamos directamente a la salida
            output_queue.append(Symbol(char, "operand"))
        elif char in precedence:  # Si es un operador
            while (operator_stack and
                   operator_stack[-1].name != '(' and
                   (precedence[operator_stack[-1].name] > precedence[char] or
                   (precedence[operator_stack[-1].name] == precedence[char] and associativity[char] == "left"))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(Symbol(char, "operator"))
        elif char == '(':  # Paréntesis izquierdo, se apila
            operator_stack.append(Symbol(char, "parenthesis"))
        elif char == ')':  # Paréntesis derecho, desapilar hasta encontrar '('
            while operator_stack and operator_stack[-1].name != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()  # Eliminar '(' de la pila

    # Vaciar lo que queda en la pila de operadores
    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue
