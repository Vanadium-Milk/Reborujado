# About
This language serves as a demostration of programming languages interpretation using different types of automata for a context free grammar, its current purpose is only experimentation and demostrating applications of the theory.

Reborujado is a typed interpreted language with basic features, it can execute basic scripts using functions and common flows, its core feature is that it makes your script look as if someone from my hometown were giving instructions to the computer.

# Usage
The interpreter is made entirely in python 3.12.3, it doesn't require dependencies nor external libraries, simply execute the [interpreter file](interpret_input.py) and then type the path to your reborujado script.

The syntax is fairly easy as it is based on c++ but without the advanced features of course, you only have to change some of the reserved words, here are some equivalences:
### Data types
- int -> acabalado
- float -> mochao
- string -> mecate
- boolean -> siono
- void -> nomas (for function declaration)
#### Flows
- if(a){} else if(b){} else{} -> dizque(a)tonces{} perosi(b)tonces{} pasino{}
- while(a){} -> ondes(a){b}
- do{} while(a) -> hacer{} ondes(a)
- for(i=a; i<b; i++){} -> patodos(i, i<b, i++){}
- void func(int a, float b){} -> chamba nomas func(acabalado a, mochao b){}
- func(); -> fonear func();
- return a; -> tornachile a;
- cout << "Hello world!"; -> disir("Qué rollo plebada!");

You don't need to create an entry point, it will just do whatever you throw at the beginning.

# Support
Saddly this project will not recieve regular maintainance, it's only an experiment to see how far can I go with a language built from scratch, if you wish to contribute to it you're more than welcome, and also consider using my interpreter to build your own language.
