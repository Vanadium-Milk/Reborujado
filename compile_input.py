from language_definition import *
from time import perf_counter

#File with rover commands
input_file = open(input("Select a file to interpret: "),"r").read()

start = perf_counter()

tokenized = token_reader.tokenize(input_file, [" ", "\n"])

#Change tokens marked as "reserved tokens" to their actual reserved word
valid = True
for token in tokenized:

    if token[1] == "no reconocido":
        raise RuntimeError(f"Error: {token[0]} is not recognized")
        
    else:
        if token[0] in RESERVED_TOKENS:
            token[1] = token[0]

#Validate grammar then proceed to execute command
if grammar_read.is_valid(tokenized):

    callables = interpreter.extract_functions(tokenized)

    for func in callables:
        func()

    print(f"Done in: {perf_counter() - start} s")