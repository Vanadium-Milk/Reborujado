from grammar_interpreter import push_down_automata
from data_types import data_type, chamba
from types import FunctionType
from typing import Mapping

class semantics_interpreter:

    sentences: set[int]
    expressions: set[int]
    constants: dict
    grammar_interpreter: push_down_automata
    function_mapping: dict[str, FunctionType]
    data_types: dict

    variables: dict[str, data_type]
    defined_functions: dict[str, chamba]

    def __init__(self,
                 grammar: push_down_automata,
                 sentences: set[int],
                 expressions: set[int],
                 functions: dict[str, FunctionType],
                 constants: dict,
                 data_types: dict) -> None:
        
        self.grammar_interpreter = grammar
        self.sentences = sentences
        self.expressions = expressions
        self.function_mapping = functions
        self.constants = constants
        self.data_types = data_types
        self.variables = {}
        self.defined_functions = {}
    
    def __pack_function(self, function: FunctionType, body: list[list[str]]) -> FunctionType:
        return lambda: function(body)
    

    def create_variable(self, id: str, value: data_type, data_type: type) -> None:
        if id in self.variables: raise RuntimeError(f"Variable: {id} already defined")

        self.variables.update({id: data_type(value)})
    
    def define_function(self, id: str, parameters: list[tuple[str, type]], commands: list[FunctionType], return_type: type):
        if id in self.defined_functions: raise RuntimeError(f"Function: {id} already defined")

        self.defined_functions.update({id: chamba(commands, parameters, return_type)})

    def modify_variable(self, id: str, value: data_type) -> None:
        if id in self.variables:
            self.variables[id].assign_value(value)
        else:
            raise RuntimeError            

    def get_variable_from_id(self, id: str):
        if not id in self.variables: raise RuntimeError(f"{id} is not defined")
            
        return self.variables[id]

    def call_function(self, id: str, arguments: list[data_type]):
        if not id in self.defined_functions: raise RuntimeError(f"{id} is not defined")

        function = self.defined_functions[id]
        variables = function.parse_arguments(arguments)
        return self.execute_locally(function.commands, variables)

    def reduce_expresion(self, tokens: list[list[str]]) -> data_type:
        
        #Remove parenthesis if no other operations are present
        if tokens[0][0] == "(" and tokens[-1][0] == ")":
            tokens = tokens[1:-1]

        #End of recursion when tokens have no right or left operand
        if len(tokens) <= 2:
            value = tokens[-1][0]
            type = tokens[-1][1]

            if type == "id":
                var = self.get_variable_from_id(value)
                
                return var
            
            if value in self.constants:
                value = self.constants[value]
            
            return self.data_types[type](value)

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
    
    def execute_locally(self, functions: list[FunctionType], local_vars: Mapping[str, data_type] = {})-> list:
        outer = [var for var in self.variables.keys()]

        #Repeated variable names are unsopported
        for var in local_vars.keys():
            if var in outer:
                raise RuntimeError("Cannot define local variable with same id as outer scope")
        
        self.variables.update(local_vars)

        #If functions have return it will pass it
        res = []
        for func in functions:
            res.append(func())

        #Remove local variables after execution
        remove = []
        for var in self.variables.keys():
            if not var in outer:
                remove.append(var)
        
        #Doing it this way to prevent the dictionary changing size during iteration
        for var in remove:
            self.variables.pop(var)
        
        return res

    def extract_functions(self, tokens: list[list[str]]) -> list[FunctionType]:
        callables = []
        
        sentn_groups = self.grammar_interpreter.get_groups(tokens, 0, self.sentences)

        for sentence in sentn_groups:
            func = self.function_mapping[sentence[0][1]]

            callables.append(self.__pack_function(func, sentence))

        return callables