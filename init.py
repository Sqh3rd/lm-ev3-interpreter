from datetime import datetime
import sys
import getopt
import os
from xmlrpc.client import DateTime
from interpreter_classes.interpreter import Interpreter
import interpreter_classes.exceptions as exceptions

def interpret(arg_input, arg_output):
    start = datetime.now()
    inter = Interpreter()
    inter.read_file(arg_input)
    inter.function_pointer, inter.class_pointer, inter.conditional_pointer, inter.comments = Interpreter.sort_lines(inter.lines, inter.comment_identifier)
    inter.functions = Interpreter.create_functions(inter.function_pointer, inter.lines, 0, 1)
    inter.classes = Interpreter.create_classes(inter.class_pointer, inter.lines, 0, 1)
    inter.conditionals = Interpreter.create_conditionals(inter.conditional_pointer, inter.lines)

    for func in inter.functions:
        func = inter.functions[func]
        temp_f, temp_cl, temp_con, temp_com = Interpreter.sort_lines(func.instructions, inter.comment_identifier)
        for e in temp_cl:
            exceptions.SyntaxError(func.line_of_decleration + e + 1, 'Cannot declare class inside function!\nWhere do you think you are?\nIn some sort of weird fever dream?\nSicko').print_err()
        for e in temp_f:
            exceptions.SyntaxError(func.line_of_decleration + e + 1, 'Cannot declare function inside function!\nNo nested function.\nCode like a sane person or leave it be.').print_err()
        func.append_nested_blocks(Interpreter.create_conditionals(temp_con, func.instructions))

    if not arg_output:
        arg_output = f"{arg_input.removesuffix(arg_input.split('.')[-1])}py"
    
    with open(arg_output, 'w') as out_file:
        out_file.write(inter.parse())

    print(f'[\033[92mOK\033[0m] Parse took {(datetime.now() - start).seconds}s')

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
    interpret(arg_input, arg_output)

if __name__ == "__main__":
    parse_args(sys.argv)