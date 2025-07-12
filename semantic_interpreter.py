from grammar_interpreter import push_down_automata
import types

class semantics_interpreter:

    sentences: list[int]
    values: list[int]
    grammar_interpreter: push_down_automata
    function_mapping: dict[str, types.FunctionType]

    def __init__(self, grammar: push_down_automata, sentences: list[int], values: list[int], functions: dict[str, types.FunctionType]) -> None:
        self.grammar_interpreter = grammar
        self.sentences = sentences
        self.values = values
        self.function_mapping = functions
    
    def __pack_function(self, function: types.FunctionType, body: list[list[str]]):
        return lambda: function(body)

    def extract_functions(self, tokens: list[list[str]]) -> list[types.FunctionType]:
        callables = []
        
        sentn_groups = self.grammar_interpreter.get_groups(tokens, 0, self.sentences)

        for sentence in sentn_groups:
            func = self.function_mapping[sentence[0][0]]

            callables.append(self.__pack_function(func, sentence + [["$", "$"]]))

        return callables