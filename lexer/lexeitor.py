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
        "regex": "(newline whitespace*)LIT<<__EOF_1__>>|(whitespace+)LIT<<__EOF_2__>>|(\"#\" [^\\n]*)LIT<<__EOF_3__>>|(integer floatnum?)LIT<<__EOF_4__>>|(floatnum)LIT<<__EOF_5__>>|(identifier)LIT<<__EOF_6__>>|(([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? '\"\"\"' ( [^\"] | '\"\"' [^\"] )* '\"\"\"')LIT<<__EOF_7__>>|(([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? \"'''\" ( [^'] | \"''\" [^'] )* \"'''\")LIT<<__EOF_8__>>|(([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? '\"'  ( [^\"\\\\\\n] | '\\\\' . )* '\"')LIT<<__EOF_9__>>|(([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? \"'\"  ( [^'\\\\\\n] | '\\\\' . )* \"'\")LIT<<__EOF_10__>>|(\"==\")LIT<<__EOF_11__>>|(\"!=\")LIT<<__EOF_12__>>|(\"<=\")LIT<<__EOF_13__>>|(\">=\")LIT<<__EOF_14__>>|(\":=\")LIT<<__EOF_15__>>|(\"->\")LIT<<__EOF_16__>>|(\"\\\\*\\\\*\")LIT<<__EOF_17__>>|(\"//\")LIT<<__EOF_18__>>|(\"\\\\+=\")LIT<<__EOF_19__>>|(\"-=\")LIT<<__EOF_20__>>|(\"\\\\*=\")LIT<<__EOF_21__>>|(\"/=\")LIT<<__EOF_22__>>|(\"%=\")LIT<<__EOF_23__>>|(\"=\")LIT<<__EOF_24__>>|(\"<\")LIT<<__EOF_25__>>|(\">\")LIT<<__EOF_26__>>|(\"+\")LIT<<__EOF_27__>>|(\"-\")LIT<<__EOF_28__>>|(\"*\")LIT<<__EOF_29__>>|(\"/\")LIT<<__EOF_30__>>|(\"%\")LIT<<__EOF_31__>>|(\"@\")LIT<<__EOF_32__>>|(\",\")LIT<<__EOF_33__>>|(\":\")LIT<<__EOF_34__>>|(\";\")LIT<<__EOF_35__>>|(\".\")LIT<<__EOF_36__>>|(\"(\")LIT<<__EOF_37__>>|(\")\")LIT<<__EOF_38__>>|(\"[\")LIT<<__EOF_39__>>|(\"]\")LIT<<__EOF_40__>>|(\"{\")LIT<<__EOF_41__>>|(\"}\")LIT<<__EOF_42__>>|(eof)LIT<<__EOF_43__>>",
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
                "integer floatnum?",
                "return \"NUMBER\""
            ],
            [
                "floatnum",
                "return \"NUMBER\""
            ],
            [
                "identifier",
                "if lxm in keywords: return keywords[lxm] return \"IDENTIFIER\""
            ],
            [
                "([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? '\"\"\"' ( [^\"] | '\"\"' [^\"] )* '\"\"\"'",
                "return \"STRING\""
            ],
            [
                "([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? \"'''\" ( [^'] | \"''\" [^'] )* \"'''\"",
                "return \"STRING\""
            ],
            [
                "([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? '\"'  ( [^\"\\\\\\n] | '\\\\' . )* '\"'",
                "return \"STRING\""
            ],
            [
                "([rRuUfFbB] | [rRuUfFbB][rRuUfFbB])? \"'\"  ( [^'\\\\\\n] | '\\\\' . )* \"'\"",
                "return \"STRING\""
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
                "return \"MOD\""
            ],
            [
                "\"@\"",
                "return \"AT\""
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
            "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":_": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":.": "frozenset({frozenset({61, 62, 63}), frozenset({48, 49, 47})})"
            },
            "frozenset({frozenset({38})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({33, 34, 55, 42, 43}), frozenset({55, 39, 40, 42, 43})})"
            },
            "frozenset({frozenset({96, 104, 105, 77, 78, 86, 87, 95})})": {
                ":\"": "frozenset({frozenset({97, 98, 100})})",
                "7:(B|F|R|U|b|f|r|u)": "frozenset({frozenset({96, 105, 78, 87})})",
                ":'": "frozenset({frozenset({106, 107, 109})})",
                ":\"\"\"": "frozenset({frozenset({80, 82, 79})})",
                ":'''": "frozenset({frozenset({88, 89, 91})})"
            },
            "frozenset({frozenset({3, 4}), frozenset({6, 7})})": {
                ":(\t| )": "frozenset({frozenset({3, 4}), frozenset({6, 7})})"
            },
            "frozenset({frozenset({33, 34, 55, 42, 43}), frozenset({55, 39, 40, 42, 43})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({39, 40, 42, 43, 44, 45, 46, 55}), frozenset({33, 34, 42, 43, 44, 45, 46, 55})})",
                ":_": "frozenset({frozenset({39, 40, 42, 43, 44, 45, 46, 55}), frozenset({33, 34, 42, 43, 44, 45, 46, 55})})"
            },
            "frozenset({frozenset({178})})": {
                "o": "frozenset({frozenset({179})})"
            },
            "frozenset({frozenset({25, 26})})": {
                "7:(0|1|2|3|4|5|6|7)": "frozenset({frozenset({55, 27, 42, 43, 28})})",
                ":_": "frozenset({frozenset({55, 27, 42, 43, 28})})"
            },
            "frozenset({frozenset({17, 13})})": {
                ":_": "frozenset({frozenset({18, 22, 55, 42, 43})})",
                "h": "frozenset({frozenset({19}), frozenset({14})})"
            },
            "frozenset({frozenset({88, 89, 91})})": {
                "01:(\t|\n|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({88, 89, 91})})",
                ":''": "frozenset({frozenset({90})})",
                ":'''": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})"
            },
            "frozenset({frozenset({90})})": {
                "01:(\t|\n|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({88, 89, 91})})"
            },
            "frozenset({frozenset({42, 43, 44, 45, 46, 55, 27, 28})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":_": "frozenset({frozenset({42, 43, 44, 45, 46, 55, 27, 28})})",
                ":.": "frozenset({frozenset({61, 62, 63}), frozenset({48, 49, 47})})",
                "7:(0|1|2|3|4|5|6|7)": "frozenset({frozenset({55, 27, 42, 43, 28})})"
            },
            "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})",
                ":_": "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})"
            },
            "frozenset({frozenset({32, 31})})": {
                ":_": "frozenset({frozenset({33, 34, 55, 42, 43}), frozenset({55, 39, 40, 42, 43})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({33, 34, 55, 42, 43}), frozenset({55, 39, 40, 42, 43})})"
            },
            "frozenset({frozenset({106, 107, 109})})": {
                "95:(\t|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({106, 107, 109})})",
                ":\\": "frozenset({frozenset({108})})",
                ":'": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})"
            },
            "frozenset({frozenset({179})})": {
                "f": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})"
            },
            "frozenset({frozenset({55, 24, 42, 43, 12, 30})})": {
                ":(,|O|o)": "frozenset({frozenset({25, 26})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":_": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":(,|X|x)": "frozenset({frozenset({17, 13})})",
                ":(,|B|b)": "frozenset({frozenset({32, 31})})"
            },
            "frozenset({frozenset({61, 62, 63}), frozenset({48, 49, 47})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({61, 62, 63}), frozenset({48, 49, 47})})",
                ":_": "frozenset({frozenset({61, 62, 63}), frozenset({48, 49, 47})})",
                ":(,|E|e)": "frozenset({frozenset({50, 51, 52, 55}), frozenset({64, 65, 66, 69})})"
            },
            "frozenset({frozenset({96, 105, 78, 87})})": {
                ":\"": "frozenset({frozenset({97, 98, 100})})",
                ":'": "frozenset({frozenset({106, 107, 109})})",
                ":\"\"\"": "frozenset({frozenset({80, 82, 79})})",
                ":'''": "frozenset({frozenset({88, 89, 91})})"
            },
            "frozenset({frozenset({81})})": {
                "99:(\t|\n|\r| |!|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({80, 82, 79})})"
            },
            "frozenset({frozenset({21}), frozenset({16})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({18, 22, 55, 42, 43})})"
            },
            "frozenset({frozenset({99})})": {
                ".": "frozenset({frozenset({97, 98, 100})})"
            },
            "frozenset({frozenset({97, 98, 100})})": {
                "93:(\t|\r| |!|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({97, 98, 100})})",
                ":\\": "frozenset({frozenset({99})})",
                ":\"": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})"
            },
            "frozenset({frozenset({37})})": {
                "n": "frozenset({frozenset({38})})"
            },
            "frozenset({frozenset({15}), frozenset({20})})": {
                "x": "frozenset({frozenset({21}), frozenset({16})})"
            },
            "frozenset({frozenset({128, 1, 2, 130, 132, 5, 134, 8, 136, 138, 11, 140, 142, 145, 147, 149, 23, 151, 153, 155, 29, 157, 159, 161, 35, 163, 165, 167, 41, 169, 171, 173, 175, 177, 56, 57, 70, 75, 76, 78, 84, 85, 87, 93, 94, 96, 102, 103, 105, 111, 113, 115, 117, 119, 121, 124, 126})})": {
                ":\\+=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":\r": "frozenset({frozenset({2})})",
                ":\n": "frozenset({frozenset({3, 4}), frozenset({6, 7})})",
                ":-=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":\\*=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":(\t| )": "frozenset({frozenset({3, 4}), frozenset({6, 7})})",
                ":/=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":#": "frozenset({frozenset({9, 10})})",
                ":%=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":0": "frozenset({frozenset({55, 24, 42, 43, 12, 30})})",
                ":<": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":": "frozenset({frozenset({143})})",
                ":+": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":-": "frozenset({frozenset({122, 148})})",
                ":*": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":/": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":%": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":@": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":,": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                "::": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":;": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                "n": "frozenset({frozenset({36})})",
                ":.": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":(": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":)": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":[": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":]": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":{": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":}": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                "e": "frozenset({frozenset({178})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":_": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({72, 73, 74, 71})})",
                "7:(B|F|R|U|b|f|r|u)": "frozenset({frozenset({96, 104, 105, 77, 78, 86, 87, 95})})",
                ":\"\"\"": "frozenset({frozenset({80, 82, 79})})",
                ":'''": "frozenset({frozenset({88, 89, 91})})",
                ":\"": "frozenset({frozenset({97, 98, 100})})",
                ":'": "frozenset({frozenset({106, 107, 109})})",
                ":==": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":!=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":<=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":>=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                "::=": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                ":\\*\\*": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                "://": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})"
            },
            "frozenset({frozenset({72, 73, 74, 71})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({72, 73, 74, 71})})",
                ":_": "frozenset({frozenset({72, 73, 74, 71})})",
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({72, 73, 74, 71})})"
            },
            "frozenset({frozenset({108})})": {
                ".": "frozenset({frozenset({106, 107, 109})})"
            },
            "frozenset({frozenset({36})})": {
                "o": "frozenset({frozenset({37})})"
            },
            "frozenset({frozenset({19}), frozenset({14})})": {
                "e": "frozenset({frozenset({15}), frozenset({20})})"
            },
            "frozenset({frozenset({42, 43, 44, 45, 46, 18, 22, 55})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":_": "frozenset({frozenset({42, 43, 44, 45, 46, 18, 22, 55})})",
                ":.": "frozenset({frozenset({61, 62, 63}), frozenset({48, 49, 47})})",
                "h": "frozenset({frozenset({19}), frozenset({14})})"
            },
            "frozenset({frozenset({2})})": {
                ":\n": "frozenset({frozenset({3, 4}), frozenset({6, 7})})"
            },
            "frozenset({frozenset({9, 10})})": {
                "98:(\t|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({9, 10})})"
            },
            "frozenset({frozenset({80, 82, 79})})": {
                ":\"\"": "frozenset({frozenset({81})})",
                ":\"\"\"": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
                "99:(\t|\n|\r| |!|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({80, 82, 79})})"
            },
            "frozenset({frozenset({55, 27, 42, 43, 28})})": {
                "7:(0|1|2|3|4|5|6|7)": "frozenset({frozenset({55, 27, 42, 43, 28})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})",
                ":_": "frozenset({frozenset({42, 43, 44, 45, 46, 55, 27, 28})})"
            },
            "frozenset({frozenset({122, 148})})": {
                ">": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})"
            },
            "frozenset({frozenset({143})})": {
                ">": "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})"
            },
            "frozenset({frozenset({39, 40, 42, 43, 44, 45, 46, 55}), frozenset({33, 34, 42, 43, 44, 45, 46, 55})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({39, 40, 42, 43, 44, 45, 46, 55}), frozenset({33, 34, 42, 43, 44, 45, 46, 55})})",
                ":_": "frozenset({frozenset({39, 40, 42, 43, 44, 45, 46, 55}), frozenset({33, 34, 42, 43, 44, 45, 46, 55})})",
                ":.": "frozenset({frozenset({61, 62, 63}), frozenset({48, 49, 47})})"
            },
            "frozenset({frozenset({50, 51, 52, 55}), frozenset({64, 65, 66, 69})})": {
                ":(+|,|-)": "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})",
                ":_": "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})"
            },
            "frozenset({frozenset({18, 22, 55, 42, 43})})": {
                "h": "frozenset({frozenset({19}), frozenset({14})})",
                ":_": "frozenset({frozenset({42, 43, 44, 45, 46, 18, 22, 55})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({44, 45, 46}), frozenset({58, 59, 60})})"
            }
        },
        "dfa_start": "frozenset({frozenset({128, 1, 2, 130, 132, 5, 134, 8, 136, 138, 11, 140, 142, 145, 147, 149, 23, 151, 153, 155, 29, 157, 159, 161, 35, 163, 165, 167, 41, 169, 171, 173, 175, 177, 56, 57, 70, 75, 76, 78, 84, 85, 87, 93, 94, 96, 102, 103, 105, 111, 113, 115, 117, 119, 121, 124, 126})})",
        "dfa_final": [
            "frozenset({frozenset({122, 148})})",
            "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})",
            "frozenset({frozenset({18, 22, 55, 42, 43})})",
            "frozenset({frozenset({3, 4}), frozenset({6, 7})})",
            "frozenset({frozenset({33, 34, 55, 42, 43}), frozenset({55, 39, 40, 42, 43})})",
            "frozenset({frozenset({39, 40, 42, 43, 44, 45, 46, 55}), frozenset({33, 34, 42, 43, 44, 45, 46, 55})})",
            "frozenset({frozenset({42, 43, 44, 45, 46, 18, 22, 55})})",
            "frozenset({frozenset({42, 43, 44, 45, 46, 55, 27, 28})})",
            "frozenset({frozenset({50, 51, 52, 55}), frozenset({64, 65, 66, 69})})",
            "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})",
            "frozenset({frozenset({55, 24, 42, 43, 12, 30})})",
            "frozenset({frozenset({55, 27, 42, 43, 28})})",
            "frozenset({frozenset({72, 73, 74, 71})})",
            "frozenset({frozenset({9, 10})})"
        ],
        "state_actions": {
            "frozenset({frozenset({3, 4}), frozenset({6, 7})})": "ACCEPT",
            "frozenset({frozenset({33, 34, 55, 42, 43}), frozenset({55, 39, 40, 42, 43})})": "ACCEPT",
            "frozenset({frozenset({42, 43, 44, 45, 46, 55, 27, 28})})": "ACCEPT",
            "frozenset({frozenset({53, 54, 55}), frozenset({51, 52, 55}), frozenset({65, 66, 69}), frozenset({67, 68, 69})})": "ACCEPT",
            "frozenset({frozenset({55, 24, 42, 43, 12, 30})})": "ACCEPT",
            "frozenset({frozenset({156}), frozenset({127}), frozenset({170}), frozenset({116}), frozenset({160}), frozenset({120}), frozenset({158}), frozenset({150}), frozenset({139}), frozenset({141}), frozenset({92}), frozenset({114}), frozenset({154}), frozenset({101}), frozenset({172}), frozenset({135}), frozenset({83}), frozenset({112}), frozenset({137}), frozenset({146}), frozenset({118}), frozenset({131}), frozenset({166}), frozenset({125}), frozenset({144}), frozenset({110}), frozenset({176}), frozenset({133}), frozenset({129}), frozenset({174}), frozenset({164}), frozenset({152}), frozenset({123}), frozenset({162}), frozenset({168}), frozenset({180})})": "ACCEPT",
            "frozenset({frozenset({72, 73, 74, 71})})": "ACCEPT",
            "frozenset({frozenset({42, 43, 44, 45, 46, 18, 22, 55})})": "ACCEPT",
            "frozenset({frozenset({9, 10})})": "ACCEPT",
            "frozenset({frozenset({55, 27, 42, 43, 28})})": "ACCEPT",
            "frozenset({frozenset({122, 148})})": "ACCEPT",
            "frozenset({frozenset({39, 40, 42, 43, 44, 45, 46, 55}), frozenset({33, 34, 42, 43, 44, 45, 46, 55})})": "ACCEPT",
            "frozenset({frozenset({50, 51, 52, 55}), frozenset({64, 65, 66, 69})})": "ACCEPT",
            "frozenset({frozenset({18, 22, 55, 42, 43})})": "ACCEPT"
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
    ",":"COMMA", ";":"SEMICOLON", "@":"AT",
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
            return text[:i], "INTEGER", i

    # 6) Categorización final
    if best_ac in (None, "unified", "ACCEPT") and best_lx is not None:
        best_ac = _categorize(best_lx)

    return best_lx, best_ac, best_ln

def scan(text: str):
    global _cur_line, _cur_col
    # No strip_comments aquí; '#' lo maneja DFA
    lines = text.splitlines(keepends=True)
    indent_stack = [0]
    out = []

    for raw in lines:
        # 1) contar espacios iniciales
        sp = 0
        while sp < len(raw) and raw[sp] == " ":
            sp += 1
        rest = raw[sp:]

        # 2) generar INDENT/DEDENT
        if rest.strip() != "":
            if sp > indent_stack[-1]:
                indent_stack.append(sp)
                out.append(("", "INDENT"))
            elif sp < indent_stack[-1]:
                while indent_stack and indent_stack[-1] > sp:
                    indent_stack.pop()
                    out.append(("", "DEDENT"))
                if indent_stack[-1] != sp:
                    raise LexerError("Error de indentación", _cur_line, sp+1)

        # 3) tokenizar la línea
        i = 0
        while i < len(rest):
            lx, ac, ln = get_token(rest[i:])
            if ln == 0:
                raise LexerError("Símbolo desconocido", _cur_line, sp + i + 1)
            frag = rest[i:i+ln]
            nl = frag.count("\n")
            if nl:
                _cur_line += nl
                _cur_col = 1 + len(frag) - frag.rfind("\n")
            else:
                _cur_col += ln

            if ac not in {"WHITESPACE","COMMENT","MULTILINE_COMMENT"}:
                out.append((lx, ac))
            i += ln

    # 4) al final, emitir DEDENT hasta el nivel 0
    while len(indent_stack) > 1:
        indent_stack.pop()
        out.append(("", "DEDENT"))

    return out


# --- trailer --------------------------------------------------