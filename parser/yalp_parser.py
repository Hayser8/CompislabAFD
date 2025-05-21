from typing import List, Set, Optional, Union
from parser.yalp_lexer import Tok
from parser.grammar import Grammar, Terminal, NonTerminal, Production

class YalpParser:
    """
    Parser de archivos .yalp para YAPar.
    Genera un objeto Grammar en BNF, ignorando agrupadores EBNF:
      - terminals: Set[Terminal]
      - non_terminals: Set[NonTerminal]
      - productions: List[Production]
      - start_symbol: NonTerminal
    """

    def __init__(self, tokens: List[Tok]) -> None:
        self.tokens: List[Tok] = tokens
        self.index: int = 0
        self.current: Optional[Tok] = tokens[0] if tokens else None

        # Nombres en crudo; luego los convertimos a objetos
        self.terminals: Set[str] = set()
        self.non_terminals: Set[str] = set()
        self.ignore_tokens: Set[str] = set()
        self.productions: List[Production] = []
        self.start_symbol_name: Optional[str] = None

    def advance(self) -> None:
        self.index += 1
        self.current = self.tokens[self.index] if self.index < len(self.tokens) else None

    def _expect(self, tok_type: str) -> None:
        if not self.current or self.current.type != tok_type:
            got = self.current.type if self.current else "EOF"
            raise SyntaxError(f"Se esperaba {tok_type}, se obtuvo {got}")
        self.advance()

    def parse(self) -> Grammar:
        """Construye la gramática leyendo las secciones de tokens y producciones."""
        self._parse_tokens_section()
        self._expect("PERCENT_PERCENT")
        self._parse_productions_section()
        return self._build_grammar()

    def _parse_tokens_section(self) -> None:
        """Analiza las directivas %token e IGNORE antes de '%%'."""
        while self.current and self.current.type != "PERCENT_PERCENT":
            if self.current.type == "PERCENT_TOKEN":
                self.advance()
                while self.current and self.current.type == "IDENTIFIER":
                    self.terminals.add(self.current.lexeme)
                    self.advance()
            elif self.current.type == "IGNORE":
                self.advance()
                if not self.current or self.current.type != "IDENTIFIER":
                    raise SyntaxError("Se esperaba IDENTIFIER después de IGNORE")
                name = self.current.lexeme
                self.ignore_tokens.add(name)
                self.terminals.add(name)
                self.advance()
            else:
                raise SyntaxError(f"Se esperaba %token o IGNORE, se obtuvo {self.current.type}")

    def _parse_productions_section(self) -> None:
        """Construye las producciones BNF ignorando agrupadores EBNF."""
        from parser.grammar import Terminal as T, NonTerminal as NT

        while self.current:
            # Cabeza de producción
            if self.current.type != "IDENTIFIER":
                raise SyntaxError(f"Se esperaba no-terminal, se obtuvo {self.current}")
            head_name = self.current.lexeme
            if self.start_symbol_name is None:
                self.start_symbol_name = head_name
            self.non_terminals.add(head_name)
            head_nt = NT(head_name)
            self.advance()

            # Dos puntos “:”
            if not self.current or self.current.lexeme != ":":
                raise SyntaxError(f"Se esperaba ':' después de {head_name}")
            self.advance()

            # Cuerpo de la producción
            body: List[Union[T, NT]] = []
            while self.current and self.current.lexeme != ";":
                # alternativa “|”
                if self.current.lexeme == "|":
                    self.productions.append(Production(
                        id=len(self.productions),
                        head=head_nt,
                        body=tuple(body)
                    ))
                    body = []
                    self.advance()
                    continue

                # agrupadores EBNF → descartar
                if self.current.lexeme in {"(", ")", "?", "*", "+"}:
                    self.advance()
                    continue

                # identificadores
                if self.current.type == "IDENTIFIER":
                    lex = self.current.lexeme
                    if lex in self.terminals:
                        body.append(T(lex))
                    else:
                        self.non_terminals.add(lex)
                        body.append(NT(lex))
                    self.advance()
                    continue

                raise SyntaxError(f"Token inesperado en cuerpo: {self.current}")

            # punto y coma “;”
            if not self.current or self.current.lexeme != ";":
                raise SyntaxError(f"Falta ';' al final de la producción de {head_name}")
            self.productions.append(Production(
                id=len(self.productions),
                head=head_nt,
                body=tuple(body)
            ))
            self.advance()

    def _build_grammar(self) -> Grammar:
        """Ensamblaje final de la gramática."""
        if not self.start_symbol_name:
            raise SyntaxError("No se encontró símbolo inicial")
        return Grammar(
            terminals={Terminal(t) for t in self.terminals},
            non_terminals={NonTerminal(nt) for nt in self.non_terminals},
            productions=self.productions,
            start_symbol=NonTerminal(self.start_symbol_name)
        )
