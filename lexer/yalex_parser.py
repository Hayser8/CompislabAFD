# YALexParser.py

class YALexParser:
    def __init__(self, filename):
        """
        Inicializa el parser y carga el archivo .yal
        """
        self.filename     = filename
        self.tokens       = {}    # name → regex
        self.rules        = {}    # rulename → list of (regex, action)
        self.header       = ""
        self.trailer      = ""
        self._header_done = False
        self._rules_done  = False
        self.parse()

    def remove_inline_comment(self, line: str) -> str:
        """
        Elimina comentarios en línea definidos entre (* y *) en una sola línea.
        """
        if "(*" in line and "*)" in line:
            return line.split("(*", 1)[0].rstrip()
        return line

    def process_rule_line(self, line: str, rule_name: str):
        """
        Procesa una línea de regla que contiene la parte de acción.
        Usa la última '{' como delimitador para separar regex de action.
        """
        idx = line.rfind("{")
        if idx == -1 or not line.rstrip().endswith("}"):
            raise SyntaxError(f"Error en la definición de regla: {line!r}")
        regex       = line[:idx].strip().lstrip("|").strip()
        action_part = line[idx+1:-1].strip()
        self.rules[rule_name].append((regex, action_part))

    def parse(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()

        current_section = None   # "header", "rule", "trailer" o None
        brace_depth     = 0
        current_rule    = None
        rule_buffer     = ""
        in_comment      = False

        for raw in raw_lines:
            stripped = raw.strip()
            if not stripped:
                continue

            # --- comentarios multilínea YALex-style (* ... *) ---
            if "(*" in stripped and "*)" in stripped:
                stripped = self.remove_inline_comment(stripped)
                if not stripped:
                    continue
            elif "(*" in stripped:
                in_comment = True
                continue
            if "*)" in stripped:
                in_comment = False
                continue
            if in_comment:
                continue

            # --- HEADER: primer bloque { ... } ---
            if not self._header_done:
                if stripped.startswith("{"):
                    current_section = "header"
                    brace_depth = stripped.count("{") - stripped.count("}")
                    self.header += raw
                    if brace_depth == 0:
                        current_section   = None
                        self._header_done = True
                    continue
            if current_section == "header":
                brace_depth += stripped.count("{") - stripped.count("}")
                self.header += raw
                if brace_depth == 0:
                    current_section   = None
                    self._header_done = True
                continue

            # --- LET definitions ---
            if stripped.startswith("let "):
                name, expr = stripped.split("=", 1)
                name  = name.strip()[4:].strip()
                regex = expr.strip()
                self.tokens[name] = regex
                continue

            # --- RULES: inicio de section rule gettoken = ---
            if stripped.startswith("rule "):
                name, expr = stripped.split("=", 1)
                rule_name = name.strip()[5:].strip()
                self.rules[rule_name] = []
                current_rule    = rule_name
                rule_buffer     = ""
                current_section = "rule"
                continue

            # --- dentro de RULE ---
            if current_section == "rule":
                ln = self.remove_inline_comment(stripped)
                if not ln:
                    continue

                # regla de una sola línea
                if "{" in ln and ln.endswith("}"):
                    self.process_rule_line(ln, current_rule)
                    continue

                # inicio de acción multilínea
                if ln.startswith("|") and "{" in ln and not ln.endswith("}"):
                    rule_buffer = ln
                    continue

                # continuación de multilínea
                if rule_buffer:
                    rule_buffer += " " + ln
                    if ln.endswith("}"):
                        self.process_rule_line(rule_buffer, current_rule)
                        rule_buffer = ""
                    continue

                # cierre de sección reglas: línea aislada "}"
                if stripped == "}":
                    current_section = None
                    self._rules_done = True
                    continue

            # --- TRAILER: siguiente bloque { ... } después de rules ---
            if self._header_done and self._rules_done and current_section is None:
                if stripped.startswith("{"):
                    current_section = "trailer"
                    brace_depth     = stripped.count("{") - stripped.count("}")
                    self.trailer += raw
                    if brace_depth == 0:
                        current_section = None
                    continue
            if current_section == "trailer":
                brace_depth += stripped.count("{") - stripped.count("}")
                self.trailer += raw
                if brace_depth == 0:
                    current_section = None
                continue

            # resto de líneas: ignorar

        if not self.rules:
            raise SyntaxError("No se encontró ninguna regla en el archivo .yal")

    def get_tokens(self):
        return self.tokens

    def get_rules(self):
        return self.rules

    def get_header(self):
        return self.header

    def get_trailer(self):
        return self.trailer
