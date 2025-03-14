class DFAG:
    def __init__(self, syntax_tree):
        """
        Construye un DFAA a partir del SyntaxTree usando el algoritmo directo:
          1) Recorrer el árbol y asignar posiciones.
          2) Calcular nullable, firstpos, lastpos, followpos.
          3) Generar estados (conjuntos de posiciones) y transiciones.
        """
        self.syntax_tree = syntax_tree
        self.states = []           # lista de conjuntos de posiciones
        self.transitions = {}      # dict: (state_id, symbol) -> new_state_id
        self.final_states = set()  # conjunto de índices de estados finales
        self.alphabet = set()      # set de símbolos que aparecen en las hojas

        # 1. Asignar posiciones e identificar hojas
        self.pos_symbol = {}
        self._assign_positions()

        # 2. Calcular nullable, firstpos, lastpos
        self._compute_nullable_first_last(self.syntax_tree.root)

        # 3. Calcular followpos
        self.followpos = {}
        # Inicializar followpos en vacío para cada posición
        for pos in range(1, self.next_pos):
            self.followpos[pos] = set()

        self._compute_followpos(self.syntax_tree.root)

        # 4. Construir DFAA (estados y transiciones)
        self._build_DFAA()

    def _assign_positions(self):
        """
        Asigna un número único a cada hoja que represente un símbolo 
        e identifica el símbolo EOF (por ejemplo, '#').
        """
        # self.next_pos se usará para llevar la cuenta de las posiciones
        self.next_pos = 1

        def assign_rec(node):
            if node.left is None and node.right is None:
                node.position = self.next_pos
    
                # Aquí guardamos la correspondencia: posición -> símbolo
                self.pos_symbol[self.next_pos] = node.value
                
                self.next_pos += 1
                
                # Agregar el símbolo al alfabeto si no es el EOF
                if node.value != '#':
                    self.alphabet.add(node.value)
            else:
                if node.left:  assign_rec(node.left)
                if node.right: assign_rec(node.right)

        assign_rec(self.syntax_tree.root)

    def _compute_nullable_first_last(self, node):
        """
        Computa nullable, firstpos y lastpos para cada nodo del árbol.
        Se asume que se recorren los hijos post-order para garantizar 
        que los hijos ya tengan computados sus valores.
        """
        if node.left is None and node.right is None:
            # Si es hoja
            node.nullable = (node.value == "ε")  # o si manejas un epsilon
            node.firstpos = {node.position} if node.value != "ε" else set()
            node.lastpos  = {node.position} if node.value != "ε" else set()
        else:
            # Asegurar que los hijos se calculen primero
            if node.left:
                self._compute_nullable_first_last(node.left)
            if node.right:
                self._compute_nullable_first_last(node.right)

            symbol = node.value  # '*', '|', '·', etc.

            if symbol == '·':  # concatenación
                node.nullable = node.left.nullable and node.right.nullable
                node.firstpos = set(node.left.firstpos)
                if node.left.nullable:
                    node.firstpos |= node.right.firstpos
                node.lastpos = set(node.right.lastpos)
                if node.right.nullable:
                    node.lastpos |= node.left.lastpos

            elif symbol == '|':  # alternación
                node.nullable = node.left.nullable or node.right.nullable
                node.firstpos = node.left.firstpos | node.right.firstpos
                node.lastpos  = node.left.lastpos  | node.right.lastpos

            elif symbol == '*':  # cerradura de Kleene
                node.nullable = True
                node.firstpos = node.left.firstpos
                node.lastpos  = node.left.lastpos

            elif symbol == '+':  # cerradura positiva
                # + se puede ver como r·(r*) => la parte base no es nullable
                node.nullable = node.left.nullable  # dep. de si r podía ser vacío
                node.firstpos = node.left.firstpos
                node.lastpos  = node.left.lastpos

            elif symbol == '?':  # opcional
                node.nullable = True
                node.firstpos = node.left.firstpos
                node.lastpos  = node.left.lastpos

            # ... otros operadores si los manejas (e.g. diferencia #)
            # Cada uno tiene sus reglas para firstpos, lastpos y nullable.

    def _compute_followpos(self, node):
        """
        Recorre el árbol para llenar followpos.
        Reglas principales:
         - Para concatenación A·B:
             Para cada posición i de lastpos(A), followpos(i) incluye firstpos(B)
         - Para cerradura * o +:
             Para cada posición i de lastpos(A), followpos(i) incluye firstpos(A)
        """
        if not node or (node.left is None and node.right is None):
            return

        symbol = node.value
        if symbol == '·':  # concatenación
            left  = node.left
            right = node.right
            for i in left.lastpos:
                self.followpos[i] |= right.firstpos

        elif symbol == '*':  # cerradura de Kleene
            # lastpos(Hijo) -> firstpos(Hijo)
            left = node.left
            for i in left.lastpos:
                self.followpos[i] |= left.firstpos

        elif symbol == '+':  # cerradura positiva
            left = node.left
            for i in left.lastpos:
                self.followpos[i] |= left.firstpos

        elif symbol == '·' or symbol == '?':
            # ya consideramos concatenación
            pass

        # Importante: recursión
        self._compute_followpos(node.left)
        self._compute_followpos(node.right)

    def _build_DFAA(self):
        """
        Construye la tabla de transiciones del DFAA usando los followpos.
         - El estado inicial es firstpos(raiz)
         - Cada vez que con un símbolo a pasamos desde el estado S a un 
           nuevo estado T, T es la unión de followpos(p) para cada posición p en S 
           cuyo símbolo sea 'a'.
        """
        # El root es la raíz del syntax tree
        root = self.syntax_tree.root
        # Estado inicial:
        start_state = frozenset(root.firstpos)
        states_list = [start_state]       # lista de sets
        self.states = [start_state]       # guardamos la misma info
        visited = set([start_state])
        state_id_map = {start_state: 0}   # asignar un ID a cada conjunto

        # Check final state: si la posición correspondiente al '#' está adentro
        # Buscamos qué posición es '#'
        # (Supongamos que la hoja con '#' la marcaste con position_#)
        hash_position = None
        # Buscamos en el árbol o en followpos
        # Podrías guardar la position del '#' en el AST, en la asignación de posiciones:
        #   if node.value == '#': self.hash_position = node.position
        # supongamos la llamas self.syntax_tree.hash_position
        if hasattr(self.syntax_tree, 'hash_position'):
            hash_position = self.syntax_tree.hash_position
        else:
            # O puedes buscarlo:
            # Este es un método rápido (no muy óptimo, pero sirve en ejemplito):
            for node in self._iter_leaves(self.syntax_tree.root):
                if node.value == '#':
                    hash_position = node.position
                    break

        # Cola para procesar (BFS)
        queue = [start_state]

        while queue:
            current_set = queue.pop(0)
            current_id = state_id_map[current_set]

            # Para cada símbolo en el alfabeto:
            for a in self.alphabet:
                # Reunimos todos los followpos de posiciones en current_set 
                # que tengan ese símbolo
                new_set = set()
                for pos in current_set:
                    # hay que determinar qué símbolo corresponde a pos
                    # en el constructor _assign_positions 
                    # (debes guardar un mapeo pos -> símbolo)
                    # supongamos lo guardamos en self.pos_symbol
                    if self.pos_symbol[pos] == a:
                        new_set |= self.followpos[pos]

                new_set = frozenset(new_set)
                if len(new_set) == 0:
                    continue  # no hay transición con 'a'
                
                if new_set not in visited:
                    visited.add(new_set)
                    states_list.append(new_set)
                    state_id_map[new_set] = len(states_list) - 1
                    queue.append(new_set)

                # Registrar la transición
                new_id = state_id_map[new_set]
                self.transitions[(current_id, a)] = new_id

        # Determinar estados finales
        for st in states_list:
            idx = state_id_map[st]
            if hash_position in st:
                self.final_states.add(idx)

    def _iter_leaves(self, node):
        """
        Generador para recorrer el árbol y retornar cada hoja.
        """
        if not node:
            return
        if node.left is None and node.right is None:
            yield node
        else:
            yield from self._iter_leaves(node.left)
            yield from self._iter_leaves(node.right)

    #
    # Nota: Falta mantener en un dict las correspondencias pos->simbolo.
    # Puedes hacerlo en _assign_positions. Ej.:
    #
    #   if node.value != '#':
    #       self.pos_symbol[node.position] = node.value
    #
    # Y si es '#', también guardarlo (así reconoces su pos).
    #

    def visualize(self, filename="DFAA_graph"):
        print("Estados del DFAA:")
        for st_id, st_set in enumerate(self.states):
            is_final = (" (final)" if st_id in self.final_states else "")
            print(f"  S{st_id} = {set(st_set)}{is_final}")
        print("\nTransiciones:")
        for (sid, symbol), tid in self.transitions.items():
            print(f"  S{sid} -- {symbol} --> S{tid}")
