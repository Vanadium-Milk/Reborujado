from grammar_interpreter import push_down_automata
import types

class semantics_interpreter:

    sentences: list[int]
    expressions: list[int]
    constants: dict
    grammar_interpreter: push_down_automata
    function_mapping: dict[str, types.FunctionType]

    def __init__(self,
                 grammar: push_down_automata,
                 sentences: list[int],
                 expressions: list[int],
                 functions: dict[str, types.FunctionType],
                 constants: dict) -> None:
        
        self.grammar_interpreter = grammar
        self.sentences = sentences
        self.expressions = expressions
        self.function_mapping = functions
        self.constants = constants
    
    def __pack_function(self, function: types.FunctionType, body: list[list[str]]):
        return lambda: function(body)

    def reduce_expresion(self, tokens: list[list[str]]):
        
        #Remove parenthesis if no other operations are present
        if tokens[0][0] == "(" and tokens[-1][0] == ")":
            tokens = tokens[1:-1]

        #End of recursion
        if len(tokens) <= 2:
            value = tokens[-1][0]

            if value in self.constants: return self.constants[value]
            else: return value

        expression = self.grammar_interpreter.get_groups(tokens, 76, self.expressions)

        left = self.reduce_expresion(expression[0])
        right = self.reduce_expresion(expression[1][1:])
        
        op = expression[1][0][0]
        operation = self.function_mapping[op]

        ans = operation(left, right)

        if len(expression) <= 2:
            return ans
        else:
            comp = self.reduce_expresion(expression[2][1:])
            
            op = expression[2][0][0]
            operation = self.function_mapping[op]

            return operation(ans, comp)
    

    def extract_functions(self, tokens: list[list[str]]) -> list[types.FunctionType]:
        callables = []
        
        sentn_groups = self.grammar_interpreter.get_groups(tokens, 0, self.sentences)

        for sentence in sentn_groups:
            func = self.function_mapping[sentence[0][0]]

            callables.append(self.__pack_function(func, sentence + [["$", "$"]]))

        return callables