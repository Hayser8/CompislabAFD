# Encabezado: Código Python que se copia en la salida
import sys
# Tabla de palabras clave reservadas
keywords = {
"if": "IF",
"else": "ELSE",
"while": "WHILE",
"return": "RETURN",
"int": "INT",
"float": "FLOAT",
"void": "VOID"
}

# --- dfa_alternatives (autogenerado) --------------------------

dfa_alternatives = [
    {
        "regex": "(whitespace+)LIT<<__EOF_1__>>|(newline)LIT<<__EOF_2__>>|(number)LIT<<__EOF_3__>>|(floatnum)LIT<<__EOF_4__>>|(identifier)LIT<<__EOF_5__>>|(('/*' ([^*] | '*' [^/])* '*' '/'))LIT<<__EOF_6__>>|('//' [^\\n]* '\\n')LIT<<__EOF_7__>>|('\"' ([^\"\\n] | '\\\\' .)* '\"')LIT<<__EOF_8__>>|('+')LIT<<__EOF_9__>>|('-')LIT<<__EOF_10__>>|('*')LIT<<__EOF_11__>>|('/')LIT<<__EOF_12__>>|('%')LIT<<__EOF_13__>>|('==')LIT<<__EOF_14__>>|('!=')LIT<<__EOF_15__>>|('<')LIT<<__EOF_16__>>|('<=')LIT<<__EOF_17__>>|('>=')LIT<<__EOF_18__>>|('>')LIT<<__EOF_19__>>|('=')LIT<<__EOF_20__>>|(';')LIT<<__EOF_21__>>|(',')LIT<<__EOF_22__>>|('(')LIT<<__EOF_23__>>|(')')LIT<<__EOF_24__>>|('{')LIT<<__EOF_25__>>|('}')LIT<<__EOF_26__>>|('[')LIT<<__EOF_27__>>|(']')LIT<<__EOF_28__>>|(eof)LIT<<__EOF_29__>>",
        "action": "unified",
        "alternatives": [
            [
                "whitespace+",
                "return \"WHITESPACE\""
            ],
            [
                "newline",
                "return \"NEWLINE\""
            ],
            [
                "number",
                "return \"INTEGER\""
            ],
            [
                "floatnum",
                "return \"FLOAT\""
            ],
            [
                "identifier",
                "if lxm in keywords: return keywords[lxm] return \"IDENTIFIER\""
            ],
            [
                "('/*' ([^*] | '*' [^/])* '*' '/')",
                "return \"MULTILINE_COMMENT\""
            ],
            [
                "'//' [^\\n]* '\\n'",
                "return \"COMMENT\""
            ],
            [
                "'\"' ([^\"\\n] | '\\\\' .)* '\"'",
                "return \"STRING\""
            ],
            [
                "'+'",
                "return \"PLUS\""
            ],
            [
                "'-'",
                "return \"MINUS\""
            ],
            [
                "'*'",
                "return \"TIMES\""
            ],
            [
                "'/'",
                "return \"DIV\""
            ],
            [
                "'%'",
                "return \"MODULO\""
            ],
            [
                "'=='",
                "return \"EQUAL\""
            ],
            [
                "'!='",
                "return \"NOT_EQUAL\""
            ],
            [
                "'<'",
                "return \"LESS_THAN\""
            ],
            [
                "'<='",
                "return \"LESS_EQUAL\""
            ],
            [
                "'>='",
                "return \"GREATER_EQUAL\""
            ],
            [
                "'>'",
                "return \"GREATER_THAN\""
            ],
            [
                "'='",
                "return \"ASSIGN\""
            ],
            [
                "';'",
                "return \"SEMICOLON\""
            ],
            [
                "','",
                "return \"COMMA\""
            ],
            [
                "'('",
                "return \"LPAREN\""
            ],
            [
                "')'",
                "return \"RPAREN\""
            ],
            [
                "'{'",
                "return \"LBRACE\""
            ],
            [
                "'}'",
                "return \"RBRACE\""
            ],
            [
                "'['",
                "return \"LBRACKET\""
            ],
            [
                "']'",
                "return \"RBRACKET\""
            ],
            [
                "eof",
                "raise(\"Fin de archivo\")"
            ]
        ],
        "dfa_transitions": {
            "frozenset({frozenset({1, 65, 67, 4, 69, 6, 71, 9, 73, 75, 77, 15, 19, 26, 30, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 59, 61, 63})})": {
                ":(\t|\r| )": "frozenset({frozenset({2, 3})})",
                ":(": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":)": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":\n": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":{": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({8, 10, 11, 7})})",
                ":}": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":[": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":]": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                "e": "frozenset({frozenset({78})})",
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({16, 17, 18})})",
                ":/*": "frozenset({frozenset({20, 21, 23})})",
                "://": "frozenset({frozenset({27, 28})})",
                ":\"": "frozenset({frozenset({32, 34, 31})})",
                ":+": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":-": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":*": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":/": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":%": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":==": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":!=": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":<": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":<=": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":>=": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":=": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":;": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                ":,": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})"
            },
            "frozenset({frozenset({13, 14})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({13, 14})})"
            },
            "frozenset({frozenset({8, 10, 11, 7})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({8, 10, 11, 7})})",
                ":.": "frozenset({frozenset({12})})"
            },
            "frozenset({frozenset({57})})": {
                ">": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})"
            },
            "frozenset({frozenset({33})})": {
                ".": "frozenset({frozenset({32, 34, 31})})"
            },
            "frozenset({frozenset({16, 17, 18})})": {
                "07:(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)": "frozenset({frozenset({16, 17, 18})})",
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({16, 17, 18})})"
            },
            "frozenset({frozenset({12})})": {
                "1:(0|1|2|3|4|5|6|7|8|9)": "frozenset({frozenset({13, 14})})"
            },
            "frozenset({frozenset({79})})": {
                "f": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})"
            },
            "frozenset({frozenset({78})})": {
                "o": "frozenset({frozenset({79})})"
            },
            "frozenset({frozenset({24, 22})})": {
                ":/": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                "99:(\t|\n|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({20, 21, 23})})"
            },
            "frozenset({frozenset({32, 34, 31})})": {
                ":\\": "frozenset({frozenset({33})})",
                ":\"": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
                "96:(\t|\r| |!|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({32, 34, 31})})"
            },
            "frozenset({frozenset({20, 21, 23})})": {
                "99:(\t|\n|\r| |!|\"|#|$|%|&|'|(|)|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({20, 21, 23})})",
                ":*": "frozenset({frozenset({24, 22})})"
            },
            "frozenset({frozenset({2, 3})})": {
                ":(\t|\r| )": "frozenset({frozenset({2, 3})})"
            },
            "frozenset({frozenset({27, 28})})": {
                "98:(\t|\r| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|~)": "frozenset({frozenset({27, 28})})",
                ":\n": "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})"
            }
        },
        "dfa_start": "frozenset({frozenset({1, 65, 67, 4, 69, 6, 71, 9, 73, 75, 77, 15, 19, 26, 30, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 59, 61, 63})})",
        "dfa_final": [
            "frozenset({frozenset({13, 14})})",
            "frozenset({frozenset({16, 17, 18})})",
            "frozenset({frozenset({2, 3})})",
            "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})",
            "frozenset({frozenset({8, 10, 11, 7})})"
        ],
        "state_actions": {
            "frozenset({frozenset({13, 14})})": "ACCEPT",
            "frozenset({frozenset({8, 10, 11, 7})})": "ACCEPT",
            "frozenset({frozenset({16, 17, 18})})": "ACCEPT",
            "frozenset({frozenset({2, 3})})": "ACCEPT",
            "frozenset({frozenset({62}), frozenset({49}), frozenset({76}), frozenset({53}), frozenset({66}), frozenset({47}), frozenset({43}), frozenset({68}), frozenset({74}), frozenset({25}), frozenset({51}), frozenset({37}), frozenset({60}), frozenset({55}), frozenset({70}), frozenset({58}), frozenset({5}), frozenset({80}), frozenset({72}), frozenset({39}), frozenset({64}), frozenset({29}), frozenset({45}), frozenset({35}), frozenset({41})})": "ACCEPT"
        }
    }
]

# --- runtime --------------------------------------------------


import re, sys

# ——————————— 1. clase de error propio ————————————
class LexerError(Exception):
    """Errores detectados durante el análisis léxico."""
    def __init__(self, msg, line, col):
        super().__init__(f"[LÉXICO] L{line}:C{col}: {msg}")
        self.line, self.column = line, col


# ——————————— 2. utilidades DFA / decode ————————————
def decode_robust_key(key: str):
    """Convierte las claves codificadas del DFA en (es_conjunto, long, charset)."""
    if key.startswith("LIT<<") and key.endswith(">>"):
        lit = key[5:-2];  return False, len(lit), {lit}
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
    """Devuelve (lexema, long, estado_final) o (None,0,None) si no hay match."""
    state, best, pos = dfa["dfa_start"], ("", 0, None), 0
    while pos < len(text):
        chunk = text[pos:]
        matched = False
        for sym, tgt in dfa["dfa_transitions"].get(state, {}).items():
            is_set, ln, charset = decode_robust_key(sym)
            if ln > len(chunk):
                continue
            probe = chunk[:ln]
            if (probe in charset) if is_set else (probe == sym):
                state, pos, matched = tgt, pos + ln, True
                if state in dfa["dfa_final"]:
                    best = (text[:pos], pos, state)
                break
        if not matched:
            break
    return best if best[1] else (None, 0, None)


# ——————————— 3. tablas rápidas ————————————
_token_map = {
    "+": "PLUS",    "-": "MINUS",    "*": "TIMES",   "/": "DIV",   "%": "MODULO",
    "==": "EQUAL",  "!=": "NOT_EQUAL",
    "<": "LESS_THAN", "<=": "LESS_EQUAL",
    ">": "GREATER_THAN", ">=": "GREATER_EQUAL",
    "=": "ASSIGN",  ";": "SEMICOLON", ",": "COMMA",
    "(": "LPAREN",  ")": "RPAREN",   "{": "LBRACE",  "}": "RBRACE",
    "[": "LBRACKET", "]": "RBRACKET"
}
_num = re.compile(r"^[0-9]+$")
_flt = re.compile(r"^[0-9]+\.[0-9]+$")
_id  = re.compile(r"^[A-Za-z_][A-Za-z_0-9]*$")


def _categorize(lxm: str):
    if lxm in keywords:   return keywords[lxm]
    if lxm in _token_map: return _token_map[lxm]
    if _num.match(lxm):   return "INTEGER"
    if _flt.match(lxm):   return "FLOAT"
    if _id.match(lxm):    return "IDENTIFIER"
    if lxm.startswith("//"): return "COMMENT"
    if lxm.startswith("/*"): return "MULTILINE_COMMENT"
    if lxm.startswith('"'):  return "STRING"
    if lxm == "\n":          return "NEWLINE"
    if all(c in " \t\r" for c in lxm): return "WHITESPACE"
    return "UNKNOWN"


# ——————————— 4. estado global de posición ————————————
_cur_line, _cur_col = 1, 1   # columnas inician en 1


# ——————————— 5. get_token con detección de errores ————————————
def get_token(text: str):
    global _cur_line, _cur_col

    best_lx, best_ac, best_ln = None, None, 0

    # 1. probar DFA
    for dfa in dfa_alternatives:
        lx, ln, st = simulate_dfa(dfa, text)
        if ln > best_ln:
            best_ln, best_lx = ln, lx
            best_ac = dfa["state_actions"].get(str(st)) or dfa["action"]

    # 2. fallbacks + detección manual de errores
    two = text[:2]

    # comentario de bloque
    if text.startswith("/*"):
        end = text.find("*/", 2)
        if end != -1:
            return text[:end+2], "MULTILINE_COMMENT", end+2
        raise LexerError("Comentario de bloque sin cerrar", _cur_line, _cur_col)

    # string
    if text.startswith('"'):
        i, escaped = 1, False
        while i < len(text):
            if not escaped and text[i] == '"':
                return text[:i+1], "STRING", i+1
            escaped = (not escaped and text[i] == '\\\\')
            i += 1
        raise LexerError("Cadena de caracteres sin comillas de cierre",
                         _cur_line, _cur_col)

    # operadores de dos caracteres
    if two in _token_map and best_ln < 2:
        return two, _token_map[two], 2

    # tokens “simples” si DFA no ayudó
    if best_ln == 0 and text:
        ch = text[0]

        if ch in _token_map:
            return ch, _token_map[ch], 1

        if ch.isalpha() or ch == "_":
            j = 1
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            lx = text[:j]
            return lx, keywords.get(lx, "IDENTIFIER"), j

        if ch.isdigit():
            i = 0
            while i < len(text) and text[i].isdigit():
                i += 1
            if i < len(text) and text[i] == ".":
                j = i + 1
                while j < len(text) and text[j].isdigit():
                    j += 1
                if j > i + 1:
                    return text[:j], "FLOAT", j
            return text[:i], "INTEGER", i

    # 3. interpretar la acción si era “unified”
    if best_ac in (None, "unified", "ACCEPT") and best_lx is not None:
        best_ac = _categorize(best_lx)

    return best_lx, best_ac, best_ln


# ——————————— 6. scan con actualización línea/col ————————————
def scan(text: str):
    global _cur_line, _cur_col
    out, i = [], 0
    SKIP = {"WHITESPACE", "NEWLINE", "COMMENT", "MULTILINE_COMMENT"}

    while i < len(text):
        lx, ac, ln = get_token(text[i:])

        if ln == 0:
            raise LexerError("Símbolo desconocido", _cur_line, _cur_col)

        # actualizar contadores de posición
        segmento = text[i:i+ln]
        nl = segmento.count("\n")
        if nl:
            _cur_line += nl
            _cur_col = 1 + len(segmento) - segmento.rfind("\n")
        else:
            _cur_col += ln

        if ac not in SKIP:
            out.append((lx, ac))

        i += ln

    return out


# --- trailer --------------------------------------------------

# Trailer: Código que se agrega al final del archivo generado
print("Fin de análisis léxico")