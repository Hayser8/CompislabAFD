class YALexParser:
    def __init__(self, filename):
        """
        Inicializa el parser y carga el archivo .yal
        """
        self.filename = filename
        self.tokens = {}        # Definiciones de tokens (let)
        self.rules = {}         # Reglas léxicas (rule)
        self.header = ""        # Código opcional de header
        self.trailer = ""       # Código opcional de trailer
        self.parse()

    def remove_inline_comment(self, line):
        """
        Elimina comentarios en línea definidos entre (* y *) en una línea.
        """
        if "(*" in line and "*)" in line:
            line = line.split("(*")[0].strip()
        return line

    def process_rule_line(self, line, rule_name):
        """
        Procesa una línea de regla que contiene la parte de acción.
        Usa la última aparición de '{' como delimitador.
        """
        idx = line.rfind("{")
        if idx == -1:
            raise SyntaxError(f"Error en la definición de regla: {line}")
        regex = line[:idx].strip().lstrip("|").strip()
        action_part = line[idx+1:].strip()
        if not action_part.endswith("}"):
            raise SyntaxError(f"Error en la definición de regla: {line}")
        action = action_part[:-1].strip()
        self.rules[rule_name].append((regex, action))

    def parse(self):
        """
        Procesa el archivo YALex sin usar expresiones regulares.
        Soporta secciones de header, let, rule y trailer, y reglas en línea o en bloque.
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        current_section = None  # Puede ser: header, rule, trailer
        current_rule = None
        rule_buffer = ""        # Acumulador para reglas multilinea
        in_comment = False      # Para comentarios multilínea

        def process_rule_buffer(buffer, rule_name):
            self.process_rule_line(buffer, rule_name)

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            # Manejo de comentarios en línea (si aparecen ambos delimitadores en la misma línea)
            if "(*" in line and "*)" in line:
                line = self.remove_inline_comment(line)
                if not line:
                    continue
            elif "(*" in line:
                in_comment = True
                continue
            if "*)" in line:
                in_comment = False
                continue
            if in_comment or line.startswith("(*"):
                continue

            # Antes de manejar el cierre general, si estamos en sección de reglas y tenemos acumulado rule_buffer
            # y la línea es "}", consideramos que es el cierre del bloque multilinea.
            if current_section == "rule" and rule_buffer and line == "}":
                rule_buffer += " }"
                process_rule_buffer(rule_buffer, current_rule)
                rule_buffer = ""
                continue

            # Cierre de sección con "}" (si no es parte de regla multilinea)
            if line == "}":
                if current_section in ("header", "trailer"):
                    current_section = None
                elif current_section == "rule":
                    # Si no hay regla acumulada, cerramos la sección
                    current_section = None
                    current_rule = None
                continue

            # Inicio de header (cuando no hay sección activa)
            if line.startswith("{") and not current_section:
                current_section = "header"
                self.header += line + "\n"
                continue

            # Si estamos en header, agregar la línea
            if current_section == "header":
                self.header += line + "\n"
                continue

            # Inicio de trailer: si estamos en sección de reglas y aparece "{" se inicia trailer
            if line.startswith("{") and current_section == "rule":
                current_section = "trailer"
                self.trailer += line + "\n"
                continue

            # Si estamos en trailer, agregar la línea
            if current_section == "trailer":
                self.trailer += line + "\n"
                continue

            # Procesar LET: definiciones de tokens
            if line.startswith("let "):
                parts = line.split("=")
                if len(parts) != 2:
                    raise SyntaxError(f"Error en la declaración de let: {line}")
                token_name = parts[0].strip()[4:]
                regex = parts[1].strip()
                self.tokens[token_name] = regex
                continue

            # Procesar RULES: inicio de sección de reglas
            if line.startswith("rule "):
                parts = line.split("=")
                if len(parts) != 2:
                    raise SyntaxError(f"Error en la declaración de rule: {line}")
                current_rule = parts[0].strip()[5:].strip()
                self.rules[current_rule] = []
                rule_buffer = ""
                current_section = "rule"
                continue

            # Procesar líneas dentro de la sección de reglas
            if current_section == "rule":
                line = self.remove_inline_comment(line)
                if not line:
                    continue

                # Regla en una sola línea: "regexp { action }"
                if "{" in line and "}" in line:
                    self.process_rule_line(line, current_rule)
                    continue

                # Si la línea inicia con "|" y no contiene "}", es el inicio de una regla multilinea
                if line.startswith("|") and "{" in line and "}" not in line:
                    rule_buffer = line
                    continue

                # Si ya se está acumulando una regla multilinea, agregar la línea al buffer
                if rule_buffer:
                    rule_buffer += " " + line
                    if "}" in rule_buffer:
                        process_rule_buffer(rule_buffer, current_rule)
                        rule_buffer = ""
                    continue

        if not self.rules:
            raise SyntaxError("Error: No se encontró ninguna regla en el archivo.")

    def get_tokens(self):
        return self.tokens

    def get_rules(self):
        return self.rules

    def get_header(self):
        return self.header.strip()

    def get_trailer(self):
        return self.trailer.strip()
