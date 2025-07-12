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
    
    def __get_next_state(self, state: int, token: str) -> int:
        return self.matrix[state][self.terminals[token]]
    
    def __traverse_productions (self, start: int, curr_prod: int, token: int, data: list[list[str]]) -> bool | int:
        #Production is the number as appears un the dictionary

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
                next = self.__get_next_state(state, data[token][1])

                token = self.__traverse_productions(start, next, token, data)
                if not token:
                    return False

            #Match terminals with the current token
            elif symbol == data[token][1]:
                token += 1
            else:
                print(f"Error, expected {symbol}, found {data[token][1]}")
                return False
        
        #Successfully traveled the base production and token list
        if curr_prod == start:
            return True
        else:
            return token
    
    def __group_tokens(self, start: int, curr_prod: int, token: int, data: list[list[str]], prod_groups: list[int]):
        sentences = []

        #Ignore empty productions
        if len(self.productions[curr_prod]) == 0:
            return token, sentences
        
        for symbol in self.productions[curr_prod]:
            
            #Recursive travel all non terminal symbols
            if symbol in self.non_terminals:
                state = self.non_terminals[symbol]
                next = self.__get_next_state(state, data[token][1])

                if next in prod_groups:
                    final = self.__traverse_productions(curr_prod, next, token, data)
                    
                    sentences.append(data[token:final])
                    token = final

                else:
                    a, b = self.__group_tokens(start, next, token, data, prod_groups)
                    #Types don't check if i don't do this
                    if isinstance(a, int):
                        token = a
                        sentences += b
                    else:
                        raise TypeError

            #Match terminals with the current token
            else:
                token += 1
        
        #Successfully traveled the base production and token list
        if curr_prod == start:
            return sentences
        else:
            return token, sentences
    

    def is_valid(self, tokens: list[list[str]]) -> bool:
        res = self.__traverse_productions(0,0,0,tokens)

        if isinstance(res, bool):
            return res
        else:
            return False
    
    def get_groups(self, tokens: list[list[str]], start_prod: int, prod_groups: list[int]) -> list:
        res = self.__group_tokens(start_prod, start_prod, 0, tokens, prod_groups)

        if isinstance(res, list):
            return res
        else:
            raise TypeError