from symbol import Symbol

precedence = {
    '|': 2,
    '.': 1,
    '*': 3,
    '+': 3,
    '?': 3
}

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
    output_queue = []
    operator_stack = []
    for char in expression:
        if char.isalnum():
            output_queue.append(Symbol(char, "operand"))
        elif char in precedence:
            while (operator_stack and operator_stack[-1].name != '(' and ((precedence[operator_stack[-1].name] > precedence[char]) or (precedence[operator_stack[-1].name] == precedence[char] and associativity[char] == "left"))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(Symbol(char, "operator"))
        elif char == '(':
            operator_stack.append(Symbol(char, "parenthesis"))
        elif char == ')':
            while operator_stack and operator_stack[-1].name != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()
    while operator_stack:
        output_queue.append(operator_stack.pop())
    return output_queue
