from language_definition import *

#File with rover commands
input_file = open("input.txt","r").read()


commands = []
tokenized = token_reader.tokenize(input_file, [" ", "\n"])

#Change tokens marked as "reserved tokens" to their actual reserved word
valid = True
for token in tokenized:

    if token[1] == "no reconocido":
        valid = False

        #Exit or continue execution
        selection = input(f"Error in line: , {token[0]} is not recognized, continue and ignore command? (Y/N): ")
        if selection == "Y" or selection == "y":
            continue
        else:
            exit()
        
    else:
        if token[0] in RESERVED_TOKENS:
            token[1] = token[0]

#Validate grammar then proceed to execute command
if grammar_read.is_valid(tokenized):

    command = tokenized[0][0]

    arguments = [token[0] for token in tokenized[1:]]
    #objMapped = [objects[arg] if arg in objects else arg for arg in arguments ]

    commands.append([command, arguments])

else:
    selection = input(f"Error in line: , invalid sintax continue and ignore command? (Y/N): ")

    if selection != "Y" and selection != "y":
        exit()

callables = pseudocompiler.extract_functions(tokenized)

for func in callables:
    func()