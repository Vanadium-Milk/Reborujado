class deterministic_automata:
    transition_table: list[list]
    alphabet: dict[str, int]
    terminal_states: dict[int, str]

    def __init__(self,
                 transition_table: list[list],
                 alphabet: dict[str, int],
                 terminal_states: dict[int, str]):

        #Verifies that the transition_table has the same lenght on all lines
        alphabet_size = len(transition_table[0])
        for token in transition_table:
            if len(token) != alphabet_size:
                raise ValueError(f"Asymmetric matrix! (line: {token})")
        
        self.transition_table = transition_table
        self.alphabet = alphabet
        self.terminal_states = terminal_states

    def tokenize(self, expresion: str, delimiter: str) -> list[list[str]]:
        
        #Array with the resulting evaluated tokens
        tokens = []

        #Just to finish the sentence
        expresion += delimiter

        #Pointers
        state = 0
        read = ''
        terminal = False
        next = 0

        for char in expresion:

            if not terminal:
                #Check existance of character
                if char in self.alphabet:
                    #Change state to the one in the character column
                    next = self.transition_table[state][self.alphabet[char]]
                else:
                    #Change to the state change in last column
                    next = self.transition_table[state][-1]

                if next in self.terminal_states:
                    #Terminal state, end token
                    terminal = True
                else:
                    state = next

            if char == delimiter:
                #Add token to the list
                if terminal:
                    tokens.append([read, self.terminal_states[next]])

                #reset pointers
                state = 0
                read = ''
                terminal = False
                next = 0
            else:
                #transcribe expresions
                read += char

        return tokens