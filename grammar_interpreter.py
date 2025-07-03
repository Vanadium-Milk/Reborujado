class push_down_automata:
    non_terminals: dict[str, int]
    terminals: dict[str, int]
    productions: list[list[str]]
    matrix: list[list]

    def __init__(self, non_terminals: dict[str, int], terminals: dict[str, int], productions: list[list[str]], pred_matrix: list[list]) -> None:
        
        token_size = len(pred_matrix[0])
        for token in pred_matrix:
            if len(token) != token_size:
                raise ValueError(f"Asymmetric matrix! (line: {token})")
        
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.matrix = pred_matrix
    
    def traverse_productions (self, curr_prod: int, token: int, data: list[list[str]]):
        #Production is the number as appears un the dictionary

        #0 is an invalid exit state in the matrix
        if curr_prod == None:
            return False

        #Ignore empty productions
        if len(self.productions[curr_prod]) == 0:
            return token
        
        for symbol in self.productions[curr_prod]:
            #Check if enough tokens are present
            if len(data) <= token:
                print("Incomplete sentence!")
                return False
            
            #Recursive travel all non terminal symbols
            if symbol in self.non_terminals:
                state = self.non_terminals[symbol]

                token = self.traverse_productions(self.matrix[state][self.terminals[data[token][1]]], token, data)
                if not token:
                    return False

            #Match terminals with the current token
            elif symbol == data[token][1]:
                token += 1
            else:
                return False
        
        #Successfully traveled the base production and token list
        if curr_prod == 0:
            return True
        else:
            return token
        
    def is_valid(self, sentence_tokens: list[list[str]]) -> int | bool:
        
        return self.traverse_productions(0,0,sentence_tokens)