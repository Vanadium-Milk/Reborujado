import tokenizer as ad
import grammar_interpreter as gi
import semantic_interpreter as si
from data_types import *

#Return the value resulting from the expression pressent in the tokens
def get_exp_values(tokens: list[list[str]], production: int):
    value_exp = grammar_read.get_groups(tokens, production, {76})
    return interpreter.reduce_expresion(value_exp[0])

#Create a variable directly from the tokens list
def var_from_tokens(tokens: list[list[str]], data_type: type) -> None:
    val = get_exp_values(tokens, 13)

    interpreter.create_variable(tokens[1][0], val, data_type)
    
#Return the code blocks and the corresponding sentences within a code block structure (if, while, for)
def decompose_block(tokens: list[list[str]], prod: int) -> tuple[list, list]:

    #Subcode production is used to prevent extracting expressions within subcode
    sub_grammars = grammar_read.get_groups(tokens, prod, {75, 76})
    sentences = grammar_read.get_groups(tokens, prod, {75})

    return [cond for cond in sub_grammars if not cond in sentences], sentences

#If
def conditional(tokens: list[list[str]]):
    cond_exp, sub_blocks = decompose_block(tokens, 45)

    #Support multiple elif declarations by iterating
    for i in range(len(sub_blocks)):
        if i >= len(cond_exp) or siono(interpreter.reduce_expresion(cond_exp[i])).val:
            return interpreter.execute_locally(interpreter.extract_functions(sub_blocks[i]))

#While
def while_loop(tokens: list[list[str]]):
    cond_exp, sub_blocks = decompose_block(tokens, 58)

    functions = interpreter.extract_functions(sub_blocks[0])

    while siono(interpreter.reduce_expresion(cond_exp[0])).val:
        res = interpreter.execute_locally(functions, return_first = True)
        if res:
            return res

#Do-wile
def do_while_loop(tokens: list[list[str]]):
    cond_exp, sub_blocks = decompose_block(tokens, 59)

    functions = interpreter.extract_functions(sub_blocks[0])

    while True:
        interpreter.execute_locally(functions)
        if not siono(interpreter.reduce_expresion(cond_exp[0])).val:
            break

#Match
def switch(tokens: list[list[str]]):
    cond_exp, sub_blocks = decompose_block(tokens, 50)

    condition = interpreter.reduce_expresion(cond_exp[0])

    #match uses values instead of expresions, so they must be extracted from there
    sub_grammars = grammar_read.get_groups(tokens, 50, {21, 22, 23, 24, 25, 26, 27, 28, 75, 76})
    cases = [interpreter.reduce_expresion(cond) for cond in sub_grammars if not (cond in sub_blocks or cond in cond_exp)]

    for i in range(len(sub_blocks)):
        if i >= len(cases) or condition.equal(cases[i]).val:
            interpreter.execute_locally(interpreter.extract_functions(sub_blocks[i]))
            
            break

def call_function(tokens: list[list[str]]):
    args_block = tokens[3:-1]

    if len(args_block) > 0:
        args_exp = grammar_read.get_groups(args_block, 65, {76})
        arguments = [interpreter.reduce_expresion(a) for a in args_exp]
    else:
        arguments = []

    return interpreter.call_function(tokens[1][0], arguments)

def define_function(tokens: list[list[str]]):
    id = tokens[2][0]
    function_block = grammar_read.get_groups(tokens, 60, {75}, False)[0]
    param_block = grammar_read.get_groups(tokens, 60, {61}, False)
    ret = tokens[1][0]

    functions = interpreter.extract_functions(function_block)
    return_type = interpreter.data_types[ret]

    parameters = []

    if len(param_block) > 0:
        par_types = param_block[0][::3]
        par_ids = param_block[0][1::3]

        for i in range(len(par_types)):
            parameters.append((par_ids[i][0], interpreter.data_types[par_types[i][0]]))

    interpreter.define_function(id, parameters, functions, return_type)

#For
def for_loop(tokens: list[list[str]]):
    exps, sub_blocks = decompose_block(tokens, 55)
    
    #Create a temporal variable for the iterator
    iter_id = tokens[2][0]
    iterator = {iter_id: acabalado(0)}

    functions = interpreter.extract_functions(sub_blocks[0])

    #match uses values instead of expresions, so they must be extracted from there
    change = grammar_read.get_groups(tokens, 55, {56, 57})

    if change[0][0][0] == "++":
        increment = 1
    else:
        increment = -1

    iterations = 0
    solve_exp = lambda: interpreter.reduce_expresion(exps[0])
    while siono(interpreter.execute_locally([solve_exp], iterator)).val:

        interpreter.execute_locally(functions, iterator)
        
        iterations += increment
        iterator[iter_id].assign_value(acabalado(iterations))

def import_file(tokens: list[list[str]]):
    file_name = tokens[-1][0][1:-1]
    
    function_list = callables_from_file(file_name)

    for func in function_list:
        func()

def return_val(tokens: list[list[str]]):
    return interpreter.reduce_expresion(tokens[1:])

def assign(tokens: list[list[str]]):
    interpreter.modify_variable(tokens[0][0], get_exp_values(tokens, 20))

def define_int(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, acabalado)

def define_string(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, mecate)

def define_float(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, mochao)

def define_bool(tokens: list[list[str]]) -> None:
    var_from_tokens(tokens, siono)

def output(tokens: list[list[str]]):
    print(get_exp_values(tokens, 77).val)

#Operands
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
    "acabalado": 0,
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
    "comentario": 11,
    "traigase": 12,
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
    "tornachile": 44,
    "nomas": 45,
    "$": 46,
    "tonces": None,
    "{": None,
    "=": None,
    "el": None
}

token_reader = ad.deterministic_automata(
    [
        [1, 6, 200, 4, 2, 8, 10, 11, 8, 0, 0, 200], #start
        [1, 201, 3, 201, 101, 101, 101, 101, 101, 101, 101, 201], #-|ε, 0-9^n
        [1, 104, 104, 104, 104, 9, 104, 9, 9, 104, 104, 200], #-
        [7, 202, 202, 202, 202, 202, 202, 202, 202, 202, 202, 202], #-|ε, 0-9^n, .
        [4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4], #", any^n
        [203, 203, 203, 203, 103, 103, 103, 103, 103, 103, 103, 203], #", any^n, "
        [6, 6, 200, 200, 100, 100, 100, 100, 100, 100, 100, 200],#(a-z|A-Z|_)^n
        [7, 202, 202, 202, 102, 102, 102, 102, 102, 102, 102, 202], #-|ε, 0-9^n, ., 0-9^n
        [104, 104, 104, 104, 104, 9, 104, 9, 9, 104, 104, 200], #=|>|<|*|+|!
        [104, 104, 104, 104, 104, 200, 104, 200, 200, 104, 104, 200], #(=|>|<|-|+|*|!)^2 | (/, =|>|<|-|+|!) 
        [104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 200], #(|)|/|*|;|+|!|{|}
        [104, 104, 104, 104, 104, 9, 104, 12, 13, 104, 104, 200], #/
        [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 105, 12], #/,/, any^n
        [13, 13, 13, 13, 13, 13, 13, 13, 14, 13, 13, 13], #/, * any^n
        [13, 13, 13, 13, 13, 13, 13, 15, 13, 13, 13, 13], #/, *, any^n, *
        [105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105] #/ *, any^n, *, /
    ],
    {
        '0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0,
        '_':1, 'a':1, 'b':1, 'c':1, 'd':1, 'e':1, 'f':1, 'g':1, 'h':1, 'i':1, 'j':1, 'k':1, 'l':1, 'm':1, 'n':1, 'o':1, 'p':1,
        'q':1, 'r':1, 's':1, 't':1, 'u':1, 'v':1, 'w':1, 'x':1, 'y':1, 'z':1, 'A':1, 'B':1, 'C':1, 'D':1, 'E':1, 'F':1, 'G':1,
        'H':1, 'I':1, 'J':1, 'K':1, 'L':1, 'M':1, 'N':1, 'O':1, 'P':1, 'Q':1, 'R':1, 'S':1, 'T':1, 'U':1, 'V':1, 'W':1, 'X':1,
        'Y':1, 'Z':1,
        '.':2,
        '"':3,
        '-':4,
        '=':5, '>':5, '<':5, '+':5, '!':5,
        '(':6, ')':6, '{':6, '}':6, ',':6, ';':6,
        '/':7,
        '*':8,
        #Delimiters
        ' ':9, '$':9,
        '\n':10
    },
    {
        100: 'id',
        101: 'entero',
        102: 'flotante',
        103: 'cadena',
        104: 'operando',
        105: 'comentario'
    },
    {
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
        "RELACIONAL": 32,
        "TIPORETORNO": 33,
        "IMPORTAR": 34
    },
    RESERVED_TOKENS,
    [
        ["EMPEZAR"], #0
        ["SENTENCIA"], #1
        ["COMENTARIO"], #2
        ["comentario", "EMPEZAR"], #3
        ["IMPORTAR", ";", "EMPEZAR"], #4
        ["DECLARACION", ";", "EMPEZAR"], #5
        ["IF", "EMPEZAR"], #6
        ["WHILE", "EMPEZAR"], #7
        ["DOWHILE", "EMPEZAR"], #8
        ["SWITCH", "EMPEZAR"], #9
        ["ASIGNACION", ";", "EMPEZAR"], #10
        ["FUNC", ";", "EMPEZAR"], #11
        ["FUNCIONDEF",  "EMPEZAR"], #12
        ["DATO", "INICIALIZACION"], #13
        ["acabalado"], #14
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
        ["chequear", "(", "EXPRESION", ")", "{", "pal", "VALOR", "{", "SUBCODIGO", "}", "CASO", "DEFAULT", "}"], #50
        ["pal", "VALOR", "{", "SUBCODIGO", "}", "CASO"], #51
        [], #52
        ["nomasno", "{", "SUBCODIGO", "}"], #53
        [], #54
        ["patodos", "(", "id", ",", "EXPRESION", ",", "CAMBIADOR", ")", "{", "SUBCODIGO", "}"], #55
        ["++"], #56
        ["--"], #57
        ["ondes", "(", "EXPRESION", ")", "{", "SUBCODIGO", "}"], #58
        ["hacer", "{", "SUBCODIGO", "}", "ondes", "(", "EXPRESION", ")",], #59
        ["chamba", "TIPORETORNO", "id", "(", "PARAMS", ")", "{", "SUBCODIGO", "}"], #60
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
        ["tornachile", "EXPRESION"], #72
        ["RETORNAR", ";", "EMPEZAR"], #73
        ["FOR", "EMPEZAR"], #74
        ["EMPEZAR"], #75
        ["VALOR", "OPERACION", "RELACIONAL"], #76
        ["disir", "(", "EXPRESION", ")"], #77
        ["ARITMETICA", "OPERACION"], #78
        ["COMPARACION"], #79
        ["DATO"], #80
        ["nomas"], #81
        ["traigase", "el", "cadena"] #82
    ],
    [
        [1,1,1,1,1,1,1,1,1,1,1,2,1,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,71,None,None,1,None,1,None,None,1,None,71],
        [None,None,None,None,None,None,None,None,None,None,None,3,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [5,5,5,5,6,7,8,9,10,11,12,None,4,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,70,None,74,None,None,73,None,None],
        [13,13,13,13,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [14,15,16,17,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,19,None,None,None,None,18,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,18],
        [None,None,None,None,None,None,None,None,20,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,26,24,None,None,None,None,21,22,23,25,25,27,28,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,29,30,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,37,None,None,None,None,None,None,None,78,78,78,78,78,78,37,37,37,37,37,37,37,None,None,None,None,None,None,37,None,None,None,None,None,37],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,44,None,None,None,None,None,None,None,None,None,None,None,None,None,44,38,39,40,41,42,43,None,None,None,None,None,None,44,None,None,None,None,None,44],
        [None,None,None,None,45,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [47,47,47,47,47,47,47,47,47,47,47,47,47,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,46,47,47,None,None,47,None,47,None,None,47,None,47],
        [49,49,49,49,49,49,49,49,49,49,49,49,49,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,48,49,None,None,49,None,49,None,None,49,None,49],
        [None,None,None,None,None,None,None,50,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,52,51,52,None,None,None,None,None,None,None,52],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,54,None,53,None,None,None,None,None,None,None,54],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,55,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,56,57,None,None,None],
        [None,None,None,None,None,58,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,59,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,60,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [61,61,61,61,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,62,None,None,None,None,None,None,None,62,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,62],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,64,None,None,None,None,None,None,None,None,None,None,None,None,63,None,None,None,None,None,64],
        [None,None,None,None,None,None,None,None,65,65,None,None,None,None,65,65,65,65,65,65,65,None,None,None,None,None,None,66,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,66],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,68,None,None,None,None,None,None,None,None,None,None,None,None,67,None,None,None,None,None,68],
        [None,None,None,None,None,None,None,None,None,69,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,72,None,None],
        [75,75,75,75,75,75,75,75,75,75,75,75,75,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,75,None,None,75,None,75,None,None,75,None,None],
        [None,None,None,None,None,None,None,None,76,76,None,None,None,None,76,76,76,76,76,76,76,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,77,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,31,32,33,34,35,36,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,None,79,None,None,None,None,None,None,None,None,None,None,None,None,None,79,79,79,79,79,79,79,None,None,None,None,None,None,79,None,None,None,None,None,79],
        [80,80,80,80,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None, 81,None],
        [None,None,None,None,None,None,None,None,None,None,None,None,82,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
    ]
)

interpreter = si.semantics_interpreter(
    grammar_read,
    {45,58,59,60,50,20,69,55,13,77,72,82},
    {38,39,40,41,42,43,31,32,33,34,35,36,21,22,23,24,25,26,27,28},
    {
        "dizque": conditional,
        "ondes": while_loop,
        "hacer": do_while_loop,
        "chequear": switch,
        "fonear": call_function,
        "chamba": define_function,
        "patodos": for_loop,
        "acabalado": define_int,
        "mochao": define_float,
        "mecate": define_string,
        "siono": define_bool,
        "disir": output,
        "id": assign,
        "tornachile": return_val,
        "traigase": import_file,
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
        "sicierto": siono(True),
        "nosierto": siono(False)
    },
    {
        #Using this instead of locate() because I want to maintain flexibility for the names
        "entero": acabalado,
        "acabalado": acabalado,
        "flotante": mochao,
        "mochao": mochao,
        "cadena": mecate,
        "mecate": mecate,
        "siono": siono,
        "sicierto": siono,
        "nosierto": siono,
        "chamba": chamba,
        "nomas": None
    }
)

def callables_from_file(input_file: str) -> list[FunctionType]:
    tokenized = token_reader.tokenize(open(input_file, "r").read(), [" ", "\n"])

    #Change tokens marked as "reserved tokens" to their actual reserved word
    for token in tokenized:

        if token[1] == "no reconocido":
            raise RuntimeError(f"Error: {token[0]} is not recognized")
            
        else:
            if token[0] in RESERVED_TOKENS:
                token[1] = token[0]
            elif token[1] == "operando":
                raise RuntimeError(f"Unrecognized operand: {token[0]}")

    #Validate grammar then proceed to execute command
    if grammar_read.is_valid(tokenized):
        return interpreter.extract_functions(tokenized)
    else:
        raise RuntimeError("File_contains errors")