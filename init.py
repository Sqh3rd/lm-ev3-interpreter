import sys
import getopt
import os
from interpreter_classes.interpreter import Interpreter

def parse_args(argv):
    arg_input = ''
    arg_output = ''
    arg_help = f'{argv[0]} -i <input> -o <output>'

    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:", ["help", "input=", "output="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        match opt:
            case "-h" | "--help":
                print(arg_help)
                sys.exit(2)
            case "-i" | "--input":
                arg_input = os.getcwd() + arg
            case "-o" | "--output":
                arg_output = os.getcwd() + arg
    
    inter = Interpreter()
    inter.read_file(arg_input)
    inter.sort_lines()
    inter.create_functions(inter.function_pointer)

    if not arg_output:
        arg_output = f"{arg_input.split('.')[-2]}.py"
    
    print(f'input: {arg_input}')
    print(f'output: {arg_output}')
    print(f'comments: {len(inter.comments)}')
    functions = '\n'.join([str(inter.functions[f]) for f in inter.functions])
    print(f'functions: {len(inter.functions)}\n{functions}')
    print(f'classes: {len(inter.classes)}')

if __name__ == "__main__":
    parse_args(sys.argv)