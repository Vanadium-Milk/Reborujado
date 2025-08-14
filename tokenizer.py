class deterministic_automata:
    transition_table: list[list]
    alphabet: dict[str, int]

    successful_terminals: dict[int, str]
    failed_terminals: dict[int, str]

    def __init__(self,
                 transition_table: list[list],
                 alphabet: dict[str, int],
                 successful_terminals: dict[int, str],
                 failed_terminals: dict[int, str]):

        #Verifies that the transition_table has the same lenght on all lines
        alphabet_size = len(transition_table[0])
        for token in transition_table:
            if len(token) != alphabet_size:
                raise ValueError(f"Asymmetric matrix! (line: {token})")
        
        self.transition_table = transition_table
        self.alphabet = alphabet
        self.successful_terminals = successful_terminals
        self.failed_terminals = failed_terminals

    def __get_transition_state(self, state: int, character: str):
        if character in self.alphabet:
            #Change state to the one in the character column
            return self.transition_table[state][self.alphabet[character]]
        else:
            #Change to the state change in last column
            return self.transition_table[state][-1]

    def tokenize(self, expresion: str, delimiters: list[str]) -> list[list[str]]:
        #Array with the resulting evaluated tokens
        tokens = []

        #Pointers
        state = 0
        read = ''
        next = 0

        for char in expresion + '$':
            next = self.__get_transition_state(state, char)

            if next in self.successful_terminals:
                #Add token to the list
                tokens.append([read, self.successful_terminals[next]])

                #reset pointers
                read = ''
                if char not in delimiters:
                    state = self.__get_transition_state(0, char)
                else:
                    state = 0

            #The token is not a valid expression
            elif next in self.failed_terminals:
                raise RuntimeError(f"{read + char}... is a {self.failed_terminals[next]}")
            else:
                state = next
            
            if char not in delimiters:
                read += char

        return tokens