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

def validate_expression(expression):
    """
    Verifica que la expresión sea válida antes de procesarla:
    - Paréntesis balanceados.
    - Caracteres permitidos.
    """
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789|.*+?()")
    stack = []
    
    for char in expression:
        if char not in valid_chars:
            raise ValueError(f"Error: Carácter inválido '{char}' en la expresión.")
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                raise ValueError("Error: Paréntesis desbalanceados, falta un '('.")
            stack.pop()
    
    if stack:
        raise ValueError("Error: Paréntesis desbalanceados, falta un ')'.")
    
def shunting_yard(expression):
    """
    Convierte una expresión regular en notación infix a postfix usando el algoritmo de Shunting Yard.
    Incluye validaciones de sintaxis antes de procesar.
    """
    validate_expression(expression)

    output_queue = []
    operator_stack = []

    for char in expression:
        if char.isalnum():
            output_queue.append(Symbol(char, "operand"))
        elif char in precedence:
            while (operator_stack and operator_stack[-1].name != '(' and
                   ((precedence[operator_stack[-1].name] > precedence[char]) or
                   (precedence[operator_stack[-1].name] == precedence[char] and associativity[char] == "left"))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(Symbol(char, "operator"))
        elif char == '(':
            operator_stack.append(Symbol(char, "parenthesis"))
        elif char == ')':
            while operator_stack and operator_stack[-1].name != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError("Error: Paréntesis desbalanceados.")
            operator_stack.pop()

    while operator_stack:
        if operator_stack[-1].name in '()':
            raise ValueError("Error: Paréntesis desbalanceados.")
        output_queue.append(operator_stack.pop())

    return output_queue
