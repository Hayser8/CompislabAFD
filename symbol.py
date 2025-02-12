class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type

    def __repr__(self):
        return self.name