import tokenizer as ad
import grammar_interpreter as gi
import semantic_interpreter as si
from data_types import *

def get_exp_values(tokens: list[list[str]], production: int):
    value_exp = grammar_read.get_groups(tokens, production, [76])
    return pseudocompiler.reduce_expresion(value_exp[0])

def var_from_tokens(tokens: list[list[str]], data_type: str) -> None:
    val = get_exp_values(tokens, 13)

    pseudocompiler.create_variable(tokens[1][0], val)    


def conditional (tokens: list[list[str]]):
    sub_grammars = grammar_read.get_groups(tokens, 45, [75, 76])
    
    cond_exp = sub_grammars[::2]
    sub_blocks = sub_grammars[1::2]

    conditions = []
    for expresions in cond_exp:
        conditions.append(pseudocompiler.reduce_expresion(expresions))

    sentences = []
    for block in sub_blocks:
        sentences.append(pseudocompiler.extract_functions(block))

    #Support multiple elif declarations by iterating
    for i in range(len(sub_blocks)):
        if conditions[i].val:
            for func in sentences[i]:
                func()
            
            break

def while_loop (tokens: list[list[str]]):
    pass

def do_while_loop (tokens: list[list[str]]):
    pass

def switch (tokens: list[list[str]]):
    pass

def call_function (tokens: list[list[str]]):
    pass

def define_function(tokens: list[list[str]]):
    pass

def for_loop (tokens: list[list[str]]):
    pass

def define_int(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, "entero")

def define_string(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, "cadena")

def define_float(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, "flotante")

def define_bool(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, "siono")

def output(tokens: list[list[str]]):
    print(get_exp_values(tokens, 77).val)

#Operands
#class conversions are only a temporal fix before adding the symbols table
def sum(a: data_type, b: data_type):
    return a.sum(b)

def subtract(a: data_type, b: data_type):
    return a.subtract(b)

def multiply(a: data_type, b: data_type):
    return a.multiply(b)

def divide(a: data_type, b: data_type):
    return a.divide(b)

def b_and(a: data_type, b: data_type):
    return a.b_and(b)

def b_or(a: data_type, b: data_type):
    return a.b_or(b)

def greater(a: data_type, b: data_type):
    return a.greater(b)

def lesser(a: data_type, b: data_type):
    return a.lesser(b)

def equal(a: data_type, b: data_type):
    return a.equal(b)

def different(a: data_type, b: data_type):
    return a.different(b)

def e_greater(a: data_type, b: data_type):
    return a.e_greater(b)

def e_lesser(a: data_type, b: data_type):
    return a.e_lesser(b)


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
    "enfierrar": 44,
    "$": 45,
    "tonces": None,
    "{": None,
    "=": None,
}

token_reader = ad.deterministic_automata(
    [
        [1, 6, 200, 4, 2, 8, 0, 200],
        [1, 201, 3, 201, 201, 201, 101, 201],
        [1, 201, 201, 201, 201, 9, 104, 201],
        [7, 202, 202, 202, 202, 202, 202, 202],
        [4, 4, 4, 5, 4, 4, 4, 4],
        [203, 203, 203, 203, 203, 203, 103, 203],
        [6, 6, 200, 200, 200, 200, 100, 200],
        [7, 202, 202, 202, 202, 202, 102, 202],
        [200, 200, 200, 200, 200, 9, 104, 200],
        [200, 200, 200, 200, 200, 200, 104, 200]
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
        '/': 5,
        '*': 5,
        ';': 5,
        '(': 5,
        ')': 5,
        '=': 5,
        '+': 5,
        '!': 5,
        '>': 5,
        '<': 5,
        '{': 5,
        '}': 5,
        ',': 5,
        '$': 5,
        #Delimiters
        ' ' : 6,
        '\n' : 6,
    },
    {
        100: 'id',
        101: 'entero',
        102: 'flotante',
        103: 'cadena',
        104: 'operando',
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
        "FUNC": 26,
        "RETORNAR": 27,
        "SUBCODIGO": 28,
        "EXPRESION": 29,
        "PRINT": 30,
        "ARITMETICA": 31,
        "RELACIONAL": 32
    },
    RESERVED_TOKENS,
    [
        ["EMPEZAR"], #0
        ["SENTENCIA"], #1
        ["COMENTARIO"], #2
        ["/*", "ANY", "*/", "EMPEZAR"], #3
        ["//", "ANY", "EMPEZAR"], #4
        ["DECLARACION", ";", "EMPEZAR"], #5
        ["IF", "EMPEZAR"], #6
        ["WHILE", "EMPEZAR"], #7
        ["DOWHILE", "EMPEZAR"], #8
        ["SWITCH", "EMPEZAR"], #9
        ["ASIGNACION", ";", "EMPEZAR"], #10
        ["FUNC", ";", "EMPEZAR"], #11
        ["FUNCIONDEF",  "EMPEZAR"], #12
        ["DATO", "INICIALIZACION"], #13
        ["completiao"], #14
        ["mochao"], #15
        ["mecate"], #16
        ["siono"], #17
        [], #18
        ["ASIGNACION"], #19
        ["id", "=", "EXPRESION"], #20
        ["entero"], #21
        ["flotante"], #22
        ["cadena"], #23
        ["FUNC"], #24
        ["BOOLEANO"], #25
        ["id"], #26
        ["(", "EXPRESION", ")"], #27
        ["voltiao", "VALOR"], #28
        ["sicierto"], #29
        ["nosierto"], #30
        ["+", "VALOR"], #31
        ["-", "VALOR"], #32
        ["*", "VALOR"], #33
        ["/", "VALOR"], #34
        ["aparte", "VALOR"], #35
        ["osino", "VALOR"], #36
        [], #37
        ["==", "VALOR", "OPERACION"], #38
        ["!=", "VALOR", "OPERACION"], #39
        [">=", "VALOR", "OPERACION"], #40
        ["<=", "VALOR", "OPERACION"], #41
        [">", "VALOR", "OPERACION"], #42
        ["<", "VALOR", "OPERACION"], #43
        [], #44
        ["dizque", "(", "EXPRESION", ")", "tonces", "{", "SUBCODIGO", "}", "IFOPCIONAL", "ELSE"], #45
        ["perosi", "(", "EXPRESION", ")", "tonces", "{", "SUBCODIGO", "}", "IFOPCIONAL"], #46
        [], #47
        ["pasino", "{", "SUBCODIGO", "}"], #48
        [], #49
        ["chequear", "(", "VALOR", ")", "{", "pal", "VALOR", "{", "SUBCODIGO", "}", "CASO", "}", "DEFAULT"], #50
        ["pal", "VALOR", "{", "SUBCODIGO", "}", "CASO"], #51
        [], #52
        ["nomasno", "{", "SUBCODIGO", "}"], #53
        [], #54
        ["patodos", "(", "EXPRESION", ",", "EXPRESION", ",", "id", "CAMBIADOR", ")", "{", "SUBCODIGO", "}"], #55
        ["++"], #56
        ["--"], #57
        ["ondes", "(", "EXPRESION", ")", "{", "SUBCODIGO", "}"], #58
        ["hacer", "{", "SUBCODIGO", "}", "ondes", "(", "EXPRESION", ")",], #59
        ["chamba", "id", "(", "PARAMS", ")", "{", "EMPEZAR", "regresar", "EXPRESION", ";"], #60
        ["DATO", "id", "PARAMSMULTIPLE"], #61
        [], #62
        [",", "DATO", "id", "PARAMSMULTIPLE"], #63
        [], #64
        ["EXPRESION", "MULTIPLE"], #65
        [], #66
        [",", "EXPRESION", "MULTIPLE"], #67
        [], #68
        ["fonear", "id", "(", "ARG", ")"], #69
        ["PRINT", ";", "EMPEZAR"], #70
        [], #71
        ["enfierrar", "EXPRESION", ";"], #72
        [], #73
        ["FOR", "EMPEZAR"], #74
        ["EMPEZAR"], #75
        ["VALOR", "OPERACION", "RELACIONAL"], #76
        ["disir", "(", "EXPRESION", ")"], #77
        ["ARITMETICA", "OPERACION"],
        ["COMPARACION"]
    ],
    [
        [1,1,1,1,1,1,1,1,1,1,1,2,2,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,71,None,None,1,None,1,None,None,71,71],
        [None,None,None,None,None,None,None,None,None,None,None,3,4,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [5,5,5,5,6,7,8,9,10,11,12,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,70,None,74,None,None,None,None],
        [13,13,13,13,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [14,15,16,17,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,19,None,None,None,None,18,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,18],
        [None,None,None,None,None,None,None,None,20,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,26,24,None,None,None,None,21,22,23,25,25,27,28,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,29,30,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,37,None,None,None,None,None,None,None,31,32,33,34,35,36,37,37,37,37,37,37,37,None,None,None,None,None,None,37,None,None,None,None,37],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,44,None,None,None,None,None,None,None,None,None,None,None,None,None,44,38,39,40,41,42,43,None,None,None,None,None,None,44,None,None,None,None,44],
        [None,None,None,None,45,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [47,47,47,47,47,47,47,47,47,47,47,47,47,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,46,47,47,None,None,47,None,47,None,None,47,47],
        [49,49,49,49,49,49,49,49,49,49,49,49,49,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,48,49,None,None,49,None,49,None,None,49,49],
        [None,None,None,None,None,None,None,50,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,52,51,None,None,None,None,None,None,None,52],
        [54,54,54,54,54,54,54,54,54,54,54,54,54,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,53,54,None,54,None,None,54,54],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,55,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,56,57,None,None],
        [None,None,None,None,None,58,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,59,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,60,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [61,61,61,61,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,62,None,None,None,None,None,None,None,62,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,62],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,64,None,None,None,None,None,None,None,None,None,None,None,None,63,None,None,None,None,64],
        [None,None,None,None,None,None,None,None,65,65,None,None,None,None,65,65,65,65,65,65,65,None,None,None,None,None,None,66,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,66],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,68,None,None,None,None,None,None,None,None,None,None,None,None,67,None,None,None,None,68],
        [None,None,None,None,None,None,None,None,None,69,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,73,None,None,None,None,None,None,None,72,73],
        [75,75,75,75,75,75,75,75,75,75,75,75,75,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,75,None,None,75,None,75,None,None,75,75],
        [None,None,None,None,None,None,None,None,76,76,None,None,None,None,76,76,76,76,76,76,76,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,77,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,31,32,33,34,35,36,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,79,None,None,None,None,None,None,None,None,None,None,None,None,None,79,79,79,79,79,79,79,None,None,None,None,None,None,79,None,None,None,None,79]
    ]
)

pseudocompiler = si.semantics_interpreter(
    grammar_read,
    [45,58,59,60,50,20,69,55,13,77],
    [38,39,40,41,42,43,31,32,33,34,35,36,21,22,23,24,25,26,27,28],
    {
        "dizque": conditional,
        "ondes": while_loop,
        "hacer": do_while_loop,
        "chequear": switch,
        "fonear": call_function,
        "chamba": define_function,
        "patodos": for_loop,
        "completiao": define_int,
        "mochao": define_float,
        "mecate": define_string,
        "siono": define_bool,
        "disir": output,
        "+": sum,
        "-": subtract,
        "*": multiply,
        "/": divide,
        "aparte": b_and,
        "osino": b_or,
        ">": greater,
        "<": lesser,
        "==": equal,
        "!=": different,
        ">=": e_greater,
        "<=": e_lesser
    },
    {
        "sicierto": True,
        "nosierto": False
    },
    {
        "entero": completiao,
        "flotante": mochao,
        "cadena": mecate,
        "siono": siono,
        "sicierto": siono,
        "nosierto": siono,
        "fonable": fonable
    }
)