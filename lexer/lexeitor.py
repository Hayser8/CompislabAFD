# ---------- HEADER: código Python incrustado ----------
import sys
# Tabla de keywords de Python
keywords = {
    "False":"FALSE", "None":"NONE", "True":"TRUE", "and":"AND", "as":"AS",
    "assert":"ASSERT", "async":"ASYNC", "await":"AWAIT", "break":"BREAK",
    "class":"CLASS", "continue":"CONTINUE", "def":"DEF", "del":"DEL",
    "elif":"ELIF", "else":"ELSE", "except":"EXCEPT", "finally":"FINALLY",
    "for":"FOR", "from":"FROM", "global":"GLOBAL", "if":"IF",
    "import":"IMPORT", "in":"IN", "is":"IS", "lambda":"LAMBDA",
    "nonlocal":"NONLOCAL", "not":"NOT", "or":"OR", "pass":"PASS",
    "raise":"RAISE", "return":"RETURN", "try":"TRY", "while":"WHILE",
    "with":"WITH", "yield":"YIELD"
}
# Para manejar INDENT/DEDENT según niveles de espacio
indent_stack = [0]
pending_dedents = []

# --- dfa_alternatives (autogenerado) --------------------------

dfa_alternatives = [
    {
        "regex": "(newline whitespace*)LIT<<__EOF_1__>>|(whitespace+)LIT<<__EOF_2__>>|(\"#\" [^\\n]*)LIT<<__EOF_3__>>|(floatnum)LIT<<__EOF_4__>>|(integer)LIT<<__EOF_5__>>|(identifier)LIT<<__EOF_6__>>|(\"==\")LIT<<__EOF_7__>>|(\"!=\")LIT<<__EOF_8__>>|(\"<=\")LIT<<__EOF_9__>>|(\">=\")LIT<<__EOF_10__>>|(\":=\")LIT<<__EOF_11__>>|(\"->\")LIT<<__EOF_12__>>|(\"\\\\*\\\\*\")LIT<<__EOF_13__>>|(\"//\")LIT<<__EOF_14__>>|(\"\\\\+=\")LIT<<__EOF_15__>>|(\"-=\")LIT<<__EOF_16__>>|(\"\\\\*=\")LIT<<__EOF_17__>>|(\"/=\")LIT<<__EOF_18__>>|(\"%=\")LIT<<__EOF_19__>>|(\"=\")LIT<<__EOF_20__>>|(\"<\")LIT<<__EOF_21__>>|(\">\")LIT<<__EOF_22__>>|(\"+\")LIT<<__EOF_23__>>|(\"-\")LIT<<__EOF_24__>>|(\"*\")LIT<<__EOF_25__>>|(\"/\")LIT<<__EOF_26__>>|(\"%\")LIT<<__EOF_27__>>|(\",\")LIT<<__EOF_28__>>|(\":\")LIT<<__EOF_29__>>|(\";\")LIT<<__EOF_30__>>|(\".\")LIT<<__EOF_31__>>|(\"(\")LIT<<__EOF_32__>>|(\")\")LIT<<__EOF_33__>>|(\"[\")LIT<<__EOF_34__>>|(\"]\")LIT<<__EOF_35__>>|(\"{\")LIT<<__EOF_36__>>|(\"}\")LIT<<__EOF_37__>>|(eof)LIT<<__EOF_38__>>",
        "action": "unified",
        "alternatives": [
            [
                "newline whitespace*",
                "# Emite un NEWLINE y luego posibles INDENT/DEDENT count_nl = yytext.count('\\n') indent   = len(yytext) - yytext.rfind('\\n') - 1 # siempre devolvemos NEWLINE primero: pending_action = (\"NEWLINE\",\"NEWLINE\") # ahora manejamos indentaci\u00f3n if indent > indent_stack[-1]: indent_stack.append(indent) pending_dedents.insert(0, (\"INDENT\",\"INDENT\")) else: while indent < indent_stack[-1]: indent_stack.pop() pending_dedents.append((\"DEDENT\",\"DEDENT\")) return pending_action"
            ],
            [
                "whitespace+",
                "/* se ignora */"
            ],
            [
                "\"#\" [^\\n]*",
                "return \"COMMENT\""
            ],
            [
                "floatnum",
                "return \"FLOAT\";"
            ],
            [
                "integer",
                "return \"INTEGER\";"
            ],
            [
                "identifier",
                "if lxm in keywords: return keywords[lxm] return \"IDENTIFIER\""
            ],
            [
                "\"==\"",
                "return \"EQ\""
            ],
            [
                "\"!=\"",
                "return \"NE\""
            ],
            [
                "\"<=\"",
                "return \"LE\""
            ],
            [
                "\">=\"",
                "return \"GE\""
            ],
            [
                "\":=\"",
                "return \"WALRUS\""
            ],
            [
                "\"->\"",
                "return \"RARROW\""
            ],
            [
                "\"\\\\*\\\\*\"",
                "return \"POW\""
            ],
            [
                "\"//\"",
                "return \"FLOORDIV\""
            ],
            [
                "\"\\\\+=\"",
                "return \"PLUSEQ\""
            ],
            [
                "\"-=\"",
                "return \"MINEQ\""
            ],
            [
                "\"\\\\*=\"",
                "return \"TIMEQ\""
            ],
            [
                "\"/=\"",
                "return \"DIVEQ\""
            ],
            [
                "\"%=\"",
                "return \"MODEQ\""
            ],
            [
                "\"=\"",
                "return \"ASSIGN\""
            ],
            [
                "\"<\"",
                "return \"LT\""
            ],
            [
                "\">\"",
                "return \"GT\""
            ],
            [
                "\"+\"",
                "return \"PLUS\""
            ],
            [
                "\"-\"",
                "return \"MINUS\""
            ],
            [
                "\"*\"",
                "return \"TIMES\""
            ],
            [
                "\"/\"",
                "return \"DIV\""
            ],
            [
                "\"%\"",
                "return \"MODULO\""
            ],
            [
                "\",\"",
                "return \"COMMA\""
            ],
            [
                "\":\"",
                "return \"COLON\""
            ],
            [
                "\";\"",
                "return \"SEMICOLON\""
            ],
            [
                "\".\"",
                "return \"DOT\""
            ],
            [
                "\"(\"",
                "return \"LPAREN\""
            ],
            [
                "\")\"",
                "return \"RPAREN\""
            ],
            [
                "\"[\"",
                "return \"LBRACKET\""
            ],
            [
                "\"]\"",
                "return \"RBRACKET\""
            ],
            [
                "\"{\"",
                "return \"LBRACE\""
            ],
            [
                "\"}\"",
                "return \"RBRACE\""
            ],
            [
                "eof",
                "# Al llegar a EOF, expulso todos los DEDENTs restantes while len(indent_stack) > 1: indent_stack.pop() pending_dedents.append((\"DEDENT\",\"DEDENT\")) if pending_dedents: return pending_dedents.pop(0) raise(\"EOF\")"
            ]
        ],
        "dfa_transitions": {
            "frozenset({frozenset({34}), frozenset({29})})": {
                "x": "frozenset({frozenset({35}), frozenset({30})})"
            },
            "frozenset({frozenset({3, 4}), frozenset({6, 7})})": {
                ":(\t| )": "frozenset({frozenset({3, 4}), frozenset({6, 7})})"
            },
            "frozenset({frozenset({51})})": {
                "n": "frozenset({frozenset({52})})"
            },
            "frozenset({frozenset({56, 26, 44, 38})})": {
                ":(,|X|x)": "frozenset({frozenset({27, 31})})",
                ":(,|B|b)": "frozenset({frozenset({45, 46})})",
                ":(,|O|o)": "frozenset({frozenset({40, 39})})"
            },
            "frozenset({frozenset({33}), frozenset({28})})": {
                "e": "frozenset({frozenset({34}), frozenset({29})})"
            },
            "frozenset({frozenset({56, 41, 42})})": {
                "7:(0|1|2|3|4|5|6|7)": "frozenset({frozenset({56, 41, 42})})",
                ":_": "frozenset({frozenset({56, 41, 42})})"
            },
            "frozenset({frozenset({1, 2, 5, 8, 11, 12, 25, 37, 43, 49, 55, 57, 62, 64, 66, 68, 70, 72, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126})})": {
                ":\r": "frozenset({frozenset({2})})",
                ":\n": "frozenset({frozenset({3, 4}), frozenset({6, 7})})",
                ":(\t| )": "frozenset({frozenset({3, 4}), frozenset({6, 7})})",
                ":#": "frozenset({frozenset({9, 10})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({13, 14, 15})})",
                ":_": "frozenset({frozenset({13, 14, 15})})",
                ":0": "frozenset({frozenset({56, 26, 44, 38})})",
                "n": "frozenset({frozenset({50})})",
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({58, 59, 60, 61})})",
                ":==": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":!=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":<=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":>=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                "::=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":-": "frozenset({frozenset({73, 99})})",
                ":\\*\\*": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                "://": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":\\+=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":-=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":\\*=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":/=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":%=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":=": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":<": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":": "frozenset({frozenset({94})})",
                ":+": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":*": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":/": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":%": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":,": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                "::": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":;": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":.": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":(": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":)": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":[": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":]": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":{": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                ":}": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
                "e": "frozenset({frozenset({127})})"
            },
            "frozenset({frozenset({128})})": {
                "f": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})"
            },
            "frozenset({frozenset({45, 46})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})",
                ":_": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})"
            },
            "frozenset({frozenset({58, 59, 60, 61})})": {
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({58, 59, 60, 61})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({58, 59, 60, 61})})",
                ":_": "frozenset({frozenset({58, 59, 60, 61})})"
            },
            "frozenset({frozenset({52})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})"
            },
            "frozenset({frozenset({127})})": {
                "o": "frozenset({frozenset({128})})"
            },
            "frozenset({frozenset({94})})": {
                ">": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})"
            },
            "frozenset({frozenset({40, 39})})": {
                ":_": "frozenset({frozenset({56, 41, 42})})",
                "7:(0|1|2|3|4|5|6|7)": "frozenset({frozenset({56, 41, 42})})"
            },
            "frozenset({frozenset({16, 17, 18})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({16, 17, 18})})",
                ":_": "frozenset({frozenset({16, 17, 18})})",
                ":(,|E|e)": "frozenset({frozenset({24, 19, 20, 21})})"
            },
            "frozenset({frozenset({13, 14, 15})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({13, 14, 15})})",
                ":_": "frozenset({frozenset({13, 14, 15})})",
                ":.": "frozenset({frozenset({16, 17, 18})})"
            },
            "frozenset({frozenset({27, 31})})": {
                "h": "frozenset({frozenset({33}), frozenset({28})})",
                ":_": "frozenset({frozenset({32, 56, 36})})"
            },
            "frozenset({frozenset({32, 56, 36})})": {
                "h": "frozenset({frozenset({33}), frozenset({28})})",
                ":_": "frozenset({frozenset({32, 56, 36})})"
            },
            "frozenset({frozenset({24, 19, 20, 21})})": {
                ":(+|,|-)": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})",
                ":_": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})"
            },
            "frozenset({frozenset({73, 99})})": {
                ">": "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})"
            },
            "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})": {
                ":_": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})"
            },
            "frozenset({frozenset({35}), frozenset({30})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({32, 56, 36})})"
            },
            "frozenset({frozenset({50})})": {
                "o": "frozenset({frozenset({51})})"
            },
            "frozenset({frozenset({2})})": {
                ":\n": "frozenset({frozenset({3, 4}), frozenset({6, 7})})"
            },
            "frozenset({frozenset({9, 10})})": {
                "98:(\t|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({9, 10})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1, 2, 5, 8, 11, 12, 25, 37, 43, 49, 55, 57, 62, 64, 66, 68, 70, 72, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126})})",
        "dfa_final": [
            "frozenset({frozenset({24, 19, 20, 21})})",
            "frozenset({frozenset({3, 4}), frozenset({6, 7})})",
            "frozenset({frozenset({32, 56, 36})})",
            "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})",
            "frozenset({frozenset({56, 26, 44, 38})})",
            "frozenset({frozenset({56, 41, 42})})",
            "frozenset({frozenset({58, 59, 60, 61})})",
            "frozenset({frozenset({73, 99})})",
            "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})",
            "frozenset({frozenset({9, 10})})"
        ],
        "state_actions": {
            "frozenset({frozenset({3, 4}), frozenset({6, 7})})": "ACCEPT",
            "frozenset({frozenset({56, 26, 44, 38})})": "ACCEPT",
            "frozenset({frozenset({56, 41, 42})})": "ACCEPT",
            "frozenset({frozenset({58, 59, 60, 61})})": "ACCEPT",
            "frozenset({frozenset({86}), frozenset({113}), frozenset({67}), frozenset({76}), frozenset({74}), frozenset({103}), frozenset({63}), frozenset({107}), frozenset({78}), frozenset({117}), frozenset({97}), frozenset({111}), frozenset({80}), frozenset({109}), frozenset({125}), frozenset({95}), frozenset({90}), frozenset({115}), frozenset({71}), frozenset({119}), frozenset({129}), frozenset({121}), frozenset({69}), frozenset({84}), frozenset({82}), frozenset({65}), frozenset({88}), frozenset({123}), frozenset({92}), frozenset({105}), frozenset({101})})": "ACCEPT",
            "frozenset({frozenset({32, 56, 36})})": "ACCEPT",
            "frozenset({frozenset({24, 19, 20, 21})})": "ACCEPT",
            "frozenset({frozenset({73, 99})})": "ACCEPT",
            "frozenset({frozenset({48, 56, 47}), frozenset({24, 20, 21}), frozenset({24, 22, 23}), frozenset({56, 53, 54})})": "ACCEPT",
            "frozenset({frozenset({9, 10})})": "ACCEPT"
        }
    }
]

# --- runtime --------------------------------------------------


import re, sys

class LexerError(Exception):
    """Errores durante el análisis léxico."""
    def __init__(self, msg, line, col):
        super().__init__(f"[LÉXICO] L{line}:C{col}: {msg}")
        self.line, self.column = line, col

def _strip_comments(text: str) -> str:
    # No eliminamos aquí; el DFA maneja '#' como token
    return text

def decode_robust_key(key: str):
    if key.startswith("LIT<<") and key.endswith(">>"):
        lit = key[5:-2]
        return False, len(lit), {lit}
    i = 0
    while i < len(key) and key[i].isdigit():
        i += 1
    if i and i < len(key) and key[i] == ":":
        body = key[i+1:]
        if body.startswith("(") and body.endswith(")"):
            return True, 1, set(body[1:-1].split("|"))
        return True, int(key[:i]), {body}
    if key.startswith(":"):
        lit = key[1:]
        if lit.startswith("(") and lit.endswith(")"):
            return True, 1, set(lit[1:-1].split("|"))
        return True, len(lit), {lit}
    return False, len(key), {key}

def simulate_dfa(dfa, text: str):
    state, best, pos = dfa["dfa_start"], ("", 0, None), 0
    while pos < len(text):
        chunk = text[pos:]
        matched = False
        for sym, tgt in dfa["dfa_transitions"].get(state, {}).items():
            is_set, ln, charset = decode_robust_key(sym)
            if ln > len(chunk): continue
            probe = chunk[:ln]
            if (probe in charset) if is_set else (probe == sym):
                state, pos, matched = tgt, pos + ln, True
                if state in dfa["dfa_final"]:
                    best = (text[:pos], pos, state)
                break
        if not matched:
            break
    return best if best[1] else (None, 0, None)

# ——— map de símbolos simples y compuestos ———
_token_map = {
    # simples
    "+":"PLUS", "-":"MINUS", "*":"TIMES", "/":"DIV", "%":"MODULO",
    "=":"ASSIGN", "<":"LT", ">":"GT", ":":"COLON", ".":"DOT",
    ",":"COMMA", ";":"SEMICOLON", 
    "(":"LPAREN", ")":"RPAREN", "[":"LBRACKET", "]":"RBRACKET",
    "{":"LBRACE", "}":"RBRACE",
    # compuestos (elipsis primero)
    "...":"ELLIPSIS",
    "==":"EQ", "!=":"NE", "<=":"LE", ">=":"GE",
    ":=":"WALRUS", "->":"RARROW",
    "**":"POW", "//":"FLOORDIV",
    "+=":"PLUSEQ", "-=":"MINEQ", "*=":"TIMEQ",
    "/=":"DIVEQ", "%=":"MODEQ",
    "**=":"POW_EQ", "//=":"FLOORDIV_EQ",
}

# Reconoce bin, oct, hex, dec con underscores y floats con exponentes
_num = re.compile(r'^(?:0[bB][01_]+|0[oO][0-7_]+|0[xX][0-9A-Fa-f_]+|\d[\d_]*)$')
_flt = re.compile(r'^(?:\d[\d_]*\.\d[\d_]*|\.\d[\d_]*|\d[\d_]*[eE][+-]?\d[\d_]*)$')
_id  = re.compile(r'^[A-Za-z_][A-Za-z_0-9]*$')

def _categorize(lxm: str):
    if lxm in keywords:     return keywords[lxm]
    if lxm in _token_map:   return _token_map[lxm]
    if "\n" in lxm:         return "NEWLINE"
    if all(c.isspace() for c in lxm): return "WHITESPACE"
    if _flt.match(lxm):     return "FLOAT"
    if _num.match(lxm):     return "INTEGER"
    if _id.match(lxm):      return "IDENTIFIER"
    return "UNKNOWN"

_cur_line, _cur_col = 1, 1

def get_token(text: str):
    global _cur_line, _cur_col

    # 0) NEWLINE puro  ── ¡antes que nada!
    if text.startswith("\r\n"):
        return "\r\n", "NEWLINE", 2          # solo CRLF
    if text[0] == "\n":
        return "\n", "NEWLINE", 1            # solo LF

    # Comentario de línea con '#'
    if text.startswith("#"):
        idx = text.find("\n")
        if idx == -1: idx = len(text)
        return text[:idx], "COMMENT", idx

    # Literales de cadena
    if text[0] in {"'", '"'}:
        quote = text[0]
        if text.startswith(quote*3):
            end_seq = quote*3
            i = 3
            while i < len(text):
                if text.startswith(end_seq, i):
                    i += 3
                    return text[:i], "STRING", i
                if text[i] == "\\" and i+1 < len(text):
                    i += 2
                else:
                    i += 1
            raise LexerError("Cadena triple sin cerrar", _cur_line, _cur_col)
        i, esc = 1, False
        while i < len(text):
            if not esc and text[i] == quote:
                return text[:i+1], "STRING", i+1
            esc = (not esc and text[i] == "\\")
            i += 1
        raise LexerError("Cadena sin cerrar", _cur_line, _cur_col)

    # 1) Elipsis '...'
    if text.startswith("..."):
        return "...", "ELLIPSIS", 3

    # 2) Literales numéricas con prefijos 0b/0o/0x y underscores
    m = re.match(r'0[bB][01_]+|0[oO][0-7_]+|0[xX][0-9A-Fa-f_]+', text)
    if m:
        lit = m.group(0)
        return lit, "INTEGER", len(lit)
    
    if text.startswith(".") and len(text) > 1 and text[1].isdigit():
        j = 2
        while j < len(text) and text[j].isdigit():
            j += 1
        return text[:j], "FLOAT", j

    # 3) DFA unificado
    best_lx, best_ac, best_ln = None, None, 0
    for dfa in dfa_alternatives:
        lx, ln, st = simulate_dfa(dfa, text)
        if ln > best_ln:
            best_ln, best_lx = ln, lx
            best_ac = dfa["state_actions"].get(str(st)) or dfa["action"]
    
    # 4) Dos caracteres
    two = text[:2]
    if two in _token_map and best_ln < 2:
        return two, _token_map[two], 2

    # 5) Fallback manual
    if best_ln == 0 and text:
        ch = text[0]
        if ch in _token_map:
            return ch, _token_map[ch], 1
        if ch.isalpha() or ch == "_":
            j = 1
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            tok = text[:j]
            return tok, keywords.get(tok, "IDENTIFIER"), j
        if ch.isdigit():
            i = 0
            while i < len(text) and text[i].isdigit():
                i += 1
            if i < len(text) and text[i] == ".":
                j = i+1
                while j < len(text) and text[j].isdigit():
                    j += 1
                if j > i+1:
                    return text[:j], "FLOAT", j
            if i < len(text) and text[i] in "eE":
                j = i + 1
                if j < len(text) and text[j] in "+-":   # signo opcional
                    j += 1
                k = j
                while k < len(text) and text[k].isdigit():
                    k += 1
                if k > j:                               # al menos un dígito
                    return text[:k], "FLOAT", k
            return text[:i], "INTEGER", i

    # 6) Categorización final
    if best_ac in (None, "unified", "ACCEPT") and best_lx is not None:
        best_ac = _categorize(best_lx)

    if best_ln == 0:
       raise LexerError("Símbolo desconocido", _cur_line, _cur_col)

    return best_lx, best_ac, best_ln

def scan(text: str):
    pos = 0
    n = len(text)
    indent_stack = [0]
    out = []
    new_line = True
    cur_line, cur_col = 1, 1

    while pos < n:
        if new_line:
            # 1) detectar indent/dedent
            start = pos
            while pos < n and text[pos] == ' ':
                pos += 1
            indent = pos - start
            if indent > indent_stack[-1] and indent % 4 == 0:
                indent_stack.append(indent)
                out.append(("", "INDENT"))
            while indent < indent_stack[-1]:
                indent_stack.pop()
                out.append(("", "DEDENT"))
            new_line = False

        # 2) extraer siguiente token
        lexeme, tok, length = get_token(text[pos:])
        if length == 0:
            raise LexerError("Símbolo desconocido", cur_line, cur_col)

        # 3) actualizar línea/columna
        lines = lexeme.split('\n')
        if len(lines) > 1:
            cur_line += len(lines) - 1
            cur_col = len(lines[-1]) + 1
            new_line = (tok == "NEWLINE")
        else:
            cur_col += length

        pos += length

        # 4) filtrar comentarios y whitespace
        if tok not in {"COMMENT", "MULTILINE_COMMENT", "WHITESPACE"}:
            out.append((lexeme, tok))

    # 5) al final, cerrar todos los niveles de indent
    # 5) al final, cerrar todos los niveles de indent
    while len(indent_stack) > 1:
        indent_stack.pop()
        out.append(("", "DEDENT"))

    # 6) siempre se emite el DEDENT raíz que exige la suite
    out.append(("", "DEDENT"))
    return out


# --- trailer --------------------------------------------------