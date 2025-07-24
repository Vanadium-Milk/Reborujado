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
    
    def __get_next_state(self, state: int, token: str) -> int | None:
        terminal = self.terminals[token]
        if terminal is None:
            return None
        else:
            return self.matrix[state][terminal]
    
    def __traverse_productions (self, start: int, curr_prod: int, token: int, data: list[list[str]]) -> int | None:
        #Production is the number as appears un the dictionary

        if curr_prod == None:
            return None

        #Ignore empty productions
        if len(self.productions[curr_prod]) == 0:
            return token
        
        for symbol in self.productions[curr_prod]:
            #Check if enough tokens are present
            if len(data) < token:
                print("Incomplete sentence!")
                return None
            
            #Recursive travel all non terminal symbols
            if symbol in self.non_terminals:
                state = self.non_terminals[symbol]
                next = self.__get_next_state(state, self.__get_data_token(data, token))

                if next is None:
                    return None
                
                res = self.__traverse_productions(start, next, token, data)
                if res is None:
                    return None
                else: token = res

            #Match terminals with the current token
            elif symbol == self.__get_data_token(data, token):
                token += 1
            else:
                print(f"Error, expected {symbol}, found {self.__get_data_token(data, token)}")
                return None
        
        #Successfully traveled the base production and token list
        return token
    
    def __group_tokens(self, start: int, curr_prod: int, token: int, data: list[list[str]], prod_groups: list[int]) -> tuple[int, list]:
        sentences = []

        #Ignore empty productions
        if len(self.productions[curr_prod]) == 0:
            return token, sentences
        
        for symbol in self.productions[curr_prod]:
            
            #Recursive travel all non terminal symbols
            if symbol in self.non_terminals:
                state = self.non_terminals[symbol]
                
                next = self.__get_next_state(state, self.__get_data_token(data, token))
                if next is None:
                    raise RuntimeError

                if next in prod_groups:
                    final = self.__traverse_productions(curr_prod, next, token, data)
                    if final:
                        sentences.append(data[token:final])
                        token = final
                    else:
                        raise RuntimeError

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
        return token, sentences

    def __get_data_token(self, data: list[list[str]], index) -> str:
        if len(data) <= index:
            return "$"
        else:
            return data[index][1]

    def is_valid(self, tokens: list[list[str]]) -> bool:
        res = self.__traverse_productions(0,0,0,tokens)

        return not res is None
    
    def get_groups(self, tokens: list[list[str]], start_prod: int, prod_groups: list[int]) -> list:
        a, res = self.__group_tokens(start_prod, start_prod, 0, tokens, prod_groups)

        if isinstance(res, list):
            return res
        else:
            raise TypeError