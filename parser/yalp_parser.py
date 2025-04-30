from typing import List
from parser.yalp_lexer import Tok
from parser.grammar import Grammar, Terminal, NonTerminal, Production

class YalpParser:
    def __init__(self, tokens: List[Tok]):
        self.tokens = tokens
        self.index = 0
        self.current = tokens[0] if tokens else None

        self.terminals = set()
        self.non_terminals = set()
        self.ignore_tokens = set()
        self.productions = []
        self.start_symbol = None

    def advance(self):
        self.index += 1
        self.current = self.tokens[self.index] if self.index < len(self.tokens) else None

    def match(self, expected_type: str):
        if self.current is None:
            raise SyntaxError(f"Se esperaba {expected_type} pero no hay más tokens")
        if self.current.type != expected_type:
            raise SyntaxError(f"Se esperaba {expected_type} en línea {self.current.line}, columna {self.current.column}, pero se encontró {self.current.type}")
        self.advance()

    def parse(self) -> Grammar:
        self.parse_tokens_section()
        self.expect_percent_percent()
        self.parse_productions_section()
        return self.build_grammar()

    def parse_tokens_section(self):
        while self.current is not None and self.current.type != "PERCENT_PERCENT":
            if self.current.type == "PERCENT_TOKEN":
                self.advance()
                while self.current is not None and self.current.type == "IDENTIFIER":
                    self.terminals.add(self.current.lexeme)
                    self.advance()
            elif self.current.type == "IGNORE":
                self.advance()
                if self.current is None or self.current.type != "IDENTIFIER":
                    raise SyntaxError(f"Se esperaba un token para ignorar después de IGNORE en línea {self.current.line}")
                self.ignore_tokens.add(self.current.lexeme)
                self.terminals.add(self.current.lexeme)
                self.advance()
            else:
                raise SyntaxError(f"Se esperaba %token o IGNORE en línea {self.current.line}, columna {self.current.column}")

    def expect_percent_percent(self):
        if self.current is None or self.current.type != "PERCENT_PERCENT":
            raise SyntaxError(f"Se esperaba %% en línea {self.current.line} columna {self.current.column}")
        self.advance()

    def parse_productions_section(self):
        while self.current is not None:
            if self.current.type != "IDENTIFIER":
                raise SyntaxError(f"Se esperaba un no-terminal en la línea {self.current.line}")

            head = self.current.lexeme
            self.non_terminals.add(head)
            if self.start_symbol is None:
                self.start_symbol = head

            self.advance()

            if self.current is None or self.current.lexeme != ":":
                raise SyntaxError(f"Se esperaba ':' después de {head} en la línea {self.current.line}")
            self.advance()

            current_body = []

            while self.current is not None and self.current.lexeme != ";":
                if self.current.lexeme == "|":
                    self.productions.append(Production(
                        id=len(self.productions),
                        head=head,
                        body=tuple(current_body)  # <- CAMBIO AQUÍ
                    ))
                    current_body = []
                    self.advance()
                elif self.current.type == "IDENTIFIER":
                    symbol = self.current.lexeme
                    if symbol in self.terminals:
                        current_body.append(Terminal(symbol))
                    else:
                        current_body.append(NonTerminal(symbol))
                    self.advance()
                else:
                    raise SyntaxError(f"Token inesperado {self.current.lexeme} en la producción de {head}")

            if self.current is None:
                raise SyntaxError(f"Se esperaba ';' para cerrar la producción de {head}")

            self.productions.append(Production(
                id=len(self.productions),
                head=head,
                body=tuple(current_body)  # <- CAMBIO AQUÍ
            ))

            self.advance()

    def build_grammar(self) -> Grammar:
        if self.start_symbol is None:
            raise SyntaxError("No se encontró símbolo inicial en el archivo.")
        
        return Grammar(
            terminals={Terminal(t) for t in self.terminals},
            non_terminals={NonTerminal(nt) for nt in self.non_terminals},
            productions=self.productions,
            start_symbol=NonTerminal(self.start_symbol)
        )
