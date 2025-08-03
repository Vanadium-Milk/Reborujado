class push_down_automata:
    non_terminals: dict[str, int]
    terminals: dict[str, int]
    productions: list[list[str]]
    matrix: list[list[int | None]]

    __traversal_cache: dict[tuple[str,...], dict[int,int]]

    def __init__(self, non_terminals: dict[str, int], terminals: dict[str, int], productions: list[list[str]], pred_matrix: list[list]) -> None:
        
        token_size = len(pred_matrix[0])
        for token in pred_matrix:
            if len(token) != token_size:
                raise ValueError(f"Asymmetric matrix! (line: {token})")
        
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.matrix = pred_matrix

        self.__traversal_cache = {}
    
    def __get_next_state(self, state: int, token: str) -> int | None:
        terminal = self.terminals[token]
        if terminal is None:
            return None
        else:
            return self.matrix[state][terminal]
    
    def __traverse_productions (self, curr_prod: int, data: list[list[str]], write_cache: bool = False) -> int:
        token = 0
        hashable = tuple([t[1] for t in data])

        if not write_cache and hashable in self.__traversal_cache:
            prods = self.__traversal_cache[hashable]
            if curr_prod in prods:
                return prods[curr_prod]

        #Ignore empty productions
        if len(self.productions[curr_prod]) == 0:
            return token
        
        for symbol in self.productions[curr_prod]:
            #Check if enough tokens are present
            if len(data) < token:
                raise RuntimeError(f"Error, expected {symbol}")
            
            #Recursive travel all non terminal symbols
            if symbol in self.non_terminals:
                state = self.non_terminals[symbol]
                next = self.__get_next_state(state, self.__get_data_token(data, token))

                if next is None:
                    raise RuntimeError(f"Error near {str([t[0] for t in data[token: token + 5]])[1:-1]}: {data[token][0]} is not a {symbol}")
                
                token += self.__traverse_productions(next, data[token:], write_cache)

            #Match terminals with the current token
            elif symbol == self.__get_data_token(data, token):
                token += 1
            else:
                raise RuntimeError(f"Error near {str([t[0] for t in data[token: token + 5]])[1:-1]}: expected {symbol}, found {self.__get_data_token(data, token)}")
        
        #Successfully traveled the base production and token list
        if write_cache:
            if hashable in self.__traversal_cache:
                self.__traversal_cache[hashable].update({curr_prod: token})
            else:
                self.__traversal_cache.update({hashable: {curr_prod: token}})

            
        return token
    
    def __group_tokens(self, start: int, curr_prod: int, token: int, data: list[list[str]], prod_groups: set[int], recursive: bool) -> tuple[int, list]:
        sentences = []

        #Ignore empty productions
        if len(self.productions[curr_prod]) == 0:
            return token, sentences
        
        #Read each simbol in the current production
        for symbol in self.productions[curr_prod]:
            #Recursive travel all non terminal symbols
            if symbol in self.non_terminals:
                state = self.non_terminals[symbol]
                
                next = self.__get_next_state(state, self.__get_data_token(data, token))

                if next is None:
                    raise RuntimeError
                
                in_group = next in prod_groups
                #Selected production is encountered, traverse to find its end and add it to the list
                if in_group or not recursive:
                    final = token + self.__traverse_productions(next, data[token:])
                    if not final: raise RuntimeError

                    if in_group:
                        sentences.append(data[token:final])
                    token = final    
                    
                #If recursive search beneath the tree for the desired productions
                else:
                    a, b = self.__group_tokens(start, next, token, data, prod_groups, True)
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
        res = self.__traverse_productions(0,tokens, True)

        return not res is None
    
    def get_groups(self, tokens: list[list[str]], start_prod: int, prod_groups: set[int], recursive: bool = True) -> list[list[list[str]]]:
        a, res = self.__group_tokens(start_prod, start_prod, 0, tokens, prod_groups, recursive)

        if isinstance(res, list):
            return res
        else:
            raise TypeError