from language_definition import callables_from_file
from time import perf_counter

#File with rover commands
input_file = input("Select a file to interpret: ")

start = perf_counter()

for func in callables_from_file(input_file):
    func()

print(f"Done in: {perf_counter() - start} s")