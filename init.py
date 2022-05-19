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
    inter.functions = Interpreter.create_functions(inter.function_pointer, inter.lines)
    inter.classes = Interpreter.create_classes(inter.class_pointer, inter.lines, inter.functions)
    inter.conditionals = Interpreter.create_conditionals(inter.conditional_pointer, inter.lines)

    if not arg_output:
        arg_output = f"{arg_input.removesuffix(arg_input.split('.')[-1])}py"
    
    print(f'comments: {len(inter.comments)}')
    print(f'functions: {len(inter.functions)}')
    print(f'classes: {len(inter.classes)}')

if __name__ == "__main__":
    parse_args(sys.argv)