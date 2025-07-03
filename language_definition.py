import tokenizer as ad
import grammar_interpreter as gi
import languaje_execution as le

RESERVED_TOKENS = {
    "completiao": 0,
    "mochao": 1,
    "mecate": 2,
    "siono": 3,
    "dizque": 4,
    "ondes": 5,
    "hacer": 6,
    "chequear": 7,
    "id": 8,
    "fonear": 9,
    "chamba": 10,
    "/*": 11,
    "//": 12,
    ";": 13,
    "entero": 14,
    "flotante": 15,
    "cadena": 16,
    "sicierto": 17,
    "nosierto": 18,
    "(": 19,
    "voltiao": 20,
    "+": 21,
    "-": 22,
    "*": 23,
    "/": 24,
    "aparte": 25,
    "osino": 26,
    ")": 27,
    "==": 28,
    "!=" : 29,
    ">=": 30,
    "<=": 31,
    ">": 32,
    "<": 33,
    "perosi": 34,
    "pasino": 35,
    "}": 36,
    "pal": 37,
    "nomasno": 38,
    "disir": 39,
    ",": 40,
    "patodos": 41,
    "++": 42,
    "--": 43,
    "$": 44,
    "tonces": None,
    "{": None
}

LANGUAGE_FUNCTIONS = {
    "dizque": le.conditional,
    "ondes": le.while_loop,
    "hacer": le.do_while_loop,
    "chequear": le.switch,
    "fonear": le.call_function,
    "chamba": le.define_function,
    "patodos": le.for_loop,
}

token_reader = ad.deterministic_automata(
    [
        [1, 6, 200, 4, 2, 200, 200],
        [1, 201, 3, 201, 201, 101, 201],
        [1, 201, 201, 201, 201, 201, 201],
        [7, 202, 202, 202, 202, 202, 202],
        [203, 4, 4, 5, 4, 4, 4],
        [203, 203, 203, 203, 203, 103, 203],
        [6, 6, 200, 200, 200, 100, 200],
        [7, 202, 202,202, 202, 102, 202]
    ],
    {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        'a': 1,
        'b': 1,
        'c': 1,
        'd': 1,
        'e': 1,
        'f': 1,
        'g': 1,
        'h': 1,
        'i': 1,
        'j': 1,
        'k': 1,
        'l': 1,
        'm': 1,
        'n': 1,
        'o': 1,
        'p': 1,
        'q': 1,
        'r': 1,
        's': 1,
        't': 1,
        'u': 1,
        'v': 1,
        'w': 1,
        'x': 1,
        'y': 1,
        'z': 1,
        'A': 1,
        'B': 1,
        'C': 1,
        'D': 1,
        'E': 1,
        'F': 1,
        'G': 1,
        'H': 1,
        'I': 1,
        'J': 1,
        'K': 1,
        'L': 1,
        'M': 1,
        'N': 1,
        'O': 1,
        'P': 1,
        'Q': 1,
        'R': 1,
        'S': 1,
        'T': 1,
        'U': 1,
        'V': 1,
        'W': 1,
        'X': 1,
        'Y': 1,
        'Z': 1,
        '.': 2,
        '"': 3,
        '-': 4,
        #Delimiters
        ' ' : 5,
        '\n' : 5,
    },
    {
        100: 'reservado',
        101: 'entero',
        102: 'flotante',
        103: 'cadena',
        200: 'no reconocido',
        201: 'entero malformado',
        202: 'flotante malformado',
        203: 'cadena malformada'
    }
)

grammar_read = gi.push_down_automata({
        "EMPEZAR": 0,
        "COMENTARIO": 1,
        "SENTENCIA": 2,
        "DECLARACION": 3,
        "DATO": 4,
        "INICIALIZACION": 5,
        "ASIGNACION": 6,
        "VALOR": 7,
        "BOOLEANO": 8,
        "OPERACION": 9,
        "COMPARACION": 10,
        "IF": 11,
        "IFOPCIONAL": 12,
        "ELSE": 13,
        "SWITCH": 14,
        "CASO": 15,
        "DEFAULT": 16,
        "FOR": 17,
        "CAMBIADOR": 18,
        "WHILE": 19,
        "DOWHILE": 20,
        "FUNCIONDEF": 21,
        "PARAMS": 22,
        "PARAMSMULTIPLE": 23,
        "ARG": 24,
        "MULTIPLE": 25,
        "FUNC": 26
    },
    RESERVED_TOKENS,
    [
        ["EMPEZAR"], #0
        ["SENTENCIA"], #1
        ["COMENTARIO"], #2
        ["/*", "ANY", "*/"], #3
        ["//", "ANY"], #4
        ["DECLARACION", ";"], #5
        ["IF"], #6
        ["WHILE"], #7
        ["DOWHILE"], #8
        ["SWITCH"], #9
        ["ASIGNACION", ";"], #10
        ["FUNC", ";"], #11
        ["FUNCIONDEF"], #12
        ["DATO", "INICIALIZACION"], #13
        ["completiao"], #14
        ["mochao"], #15
        ["mecate"], #16
        ["siono"], #17
        [], #18
        ["ASIGNACION"], #19
        ["id", "=", "VALOR", "OPERACION", "COMPARACION"], #20
        ["entero"], #21
        ["flotante"], #22
        ["cadena"], #23
        ["FUNC"], #24
        ["BOOLEANO"], #25
        ["id"], #26
        ["(", "VALOR", ")"], #27
        ["voltiao", "VALOR"], #28
        ["sicierto"], #29
        ["nosierto"], #30
        ["+", "VALOR", "OPERACION"], #31
        ["-", "VALOR", "OPERACION"], #32
        ["*", "VALOR", "OPERACION"], #33
        ["/", "VALOR", "OPERACION"], #34
        ["aparte", "VALOR", "OPERACION"], #35
        ["osino", "VALOR", "OPERACION"], #36
        [], #37
        ["==", "VALOR", "OPERACION"], #38
        ["!=", "VALOR", "OPERACION"], #39
        [">=", "VALOR", "OPERACION"], #40
        ["<=", "VALOR", "OPERACION"], #41
        [">", "VALOR", "OPERACION"], #42
        ["<", "VALOR", "OPERACION"], #43
        [], #44
        ["dizque", "(", "VALOR", "OPERACION", "COMPARACION", ")", "tonces", "{", "SENTENCIA", "}", "IFOPCIONAL", "ELSE"], #45
        ["perosi", "(", "VALOR", "OPERACION", "COMPARACION", ")", "tonces", "{", "SENTENCIA", "}", "IFOPCIONAL"], #46
        [], #47
        ["pasino", "{", "SENTENCIA", "}"], #48
        [], #49
        ["chequear", "(", "VALOR", ")", "{", "pal", "VALOR", "{", "SENTENCIA", "}", "CASO", "}", "DEFAULT"], #50
        ["pal", "VALOR", "{", "SENTENCIA", "}", "CASO"], #51
        [], #52
        ["nomasno", "{", "SENTENCIA", "}"], #53
        [], #54
        ["patodos", "(", "VALOR", "OPERACION", ",", "VALOR", "OPERACION", "COMPARACION", ",", "id", "CAMBIADOR", ")", "{", "SENTENCIA", "}"], #55
        ["++"], #56
        ["--"], #57
        ["ondes", "(", "VALOR", "OPERACION", "COMPARACION", ")", "{", "SENTENCIA", "}"], #58
        ["hacer", "{", "SENTENCIA", "}", "ondes", "(", "VALOR", "OPERACION", "COMPARACION", ")",], #59
        ["chamba", "id", "(", "PARAMS", ")", "{", "SENTENCIA", "regresar", "VALOR", "OPERACION", "COMPARACION", ";"], #60
        ["DATO", "id", "PARAMSMULTIPLE"], #61
        [], #62
        [",", "DATO", "id", "PARAMSMULTIPLE"], #63
        [], #64
        ["VALOR", "OPERACION", "COMPARACION", "MULTIPLE"], #65
        [], #66
        [",", "VALOR", "OPERACION", "COMPARACION", "MULTIPLE"], #67
        [], #68
        ["fonear", "id", "(", "ARG", ")"], #69
        ["disir", "(", "VALOR", "OPERACION", "COMPARACION", ")"], #70
    ],
    [
        [1,1,1,1,1,1,None,1,1,1,None,2,2,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,1,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,3,4,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [5,5,5,5,6,7,8,9,10,11,12,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,70,None,None,None,None,None],
        [13,13,13,13,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None, None],
        [14,15,16,17,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None, None],
        [None,None,None,None,None,None,None,None,19,None,None,None,None,18,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None, 18],
        [None,None,None,None,None,None,None,None,20,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,26,24,None,None,None,None,21,22,23,25,25,27,28,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,29,30,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,37,None,None,None,None,None,None,None,31,32,33,34,35,36,37,37,37,37,37,37,37,None,None,None,None,None,None,37,None,None,None,37],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,44,None,None,None,None,None,None,None,None,None,None,None,None,None,44,38,39,40,41,42,43,None,None,None,None,None,None,44,None,None,None,44],
        [None,None,None,None,45,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,46,47,None,None,None,None,None,None,None,None,47],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,48,None,None,None,None,None,None,None,None, 49],
        [None,None,None,None,None,None,None,50,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,52,51,None,None,None,None,None,None, 52],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,53,None,None,None,None,None, 54],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,55,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,56,57,None],
        [None,None,None,None,None,58,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,59,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,60,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [61,61,61,61,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,62,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,62],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,64,None,None,None,None,None,None,None,None,None,None,None,None,64,None,None,None,64],
        [None,None,None,None,None,None,None,None,65,65,None,None,None,None,65,65,65,65,65,65,65,None,None,None,None,None,None,66,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,66],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,68,None,None,None,None,None,None,None,None,None,None,None,None,67,None,None,None,68],
        [None,None,None,None,None,None,None,None,None,69,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
    ]
)

#File with rover commands
input_file = open("input.txt","r").readlines()


commands = []
for line in input_file:
    if line[-1] == "\n":
        line = line[:-1]
    tokenized = token_reader.tokenize(line, " ")

    #Change tokens marked as "reserved tokens" to their actual reserved word
    valid = True
    for token in tokenized:
        if token[1] == "reservado" or token[1] == "no reconocido":
            if token[0] in RESERVED_TOKENS:
                token[1] = token[0]
            #elif token[0] in objects:
            #    token[1] = "Object"
            else:
                valid = False

                #Exit or continue execution
                selection = input(f"Error in line: {line}, {token[0]} is not recognized, continue and ignore command? (Y/N): ")
                if selection == "Y" or selection == "y":
                    continue
                else:
                    exit()

    #Validate grammar then proceed to execute command
    if grammar_read.is_valid(tokenized):

        command = tokenized[0][0]

        arguments = [token[0] for token in tokenized[1:]]
        #objMapped = [objects[arg] if arg in objects else arg for arg in arguments ]

        commands.append([command, arguments])

    else:
        selection = input(f"Error in line: {line}, invalid sintax continue and ignore command? (Y/N): ")

        if selection != "Y" and selection != "y":
            exit()

#Execute all commands in order
for com in commands:
    LANGUAGE_FUNCTIONS[com[0]](com[1])