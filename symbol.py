class Symbol:
    """
    Clase para representar símbolos en expresiones regulares.
    Puede ser un operador, operando o paréntesis.
    """
    def __init__(self, name, symbol_type):
        self.name = name  
        self.type = symbol_type  

    def __repr__(self):
        return self.name
