import sys
import getopt
import os
from interpreter_classes.interpreter import Interpreter

def interpret(arg_input, arg_output):
    inter = Interpreter()
    inter.read_file(arg_input)
    inter.function_pointer, inter.class_pointer, inter.conditional_pointer, inter.comments = Interpreter.sort_lines(inter.lines, inter.comment_identifier)
    inter.functions = Interpreter.create_functions(inter.function_pointer, inter.lines)
    inter.classes = Interpreter.create_classes(inter.class_pointer, inter.lines)
    inter.conditionals = Interpreter.create_conditionals(inter.conditional_pointer, inter.lines)

    for func in inter.functions:
        func = inter.functions[func]
        temp_f, temp_cl, temp_con, temp_com = Interpreter.sort_lines(func.instructions, inter.comment_identifier)
        func.append_nested_blocks(Interpreter.create_functions(temp_f, func.instructions), Interpreter.create_classes(temp_cl, func.instructions), Interpreter.create_conditionals(temp_con, func.instructions))

    if not arg_output:
        arg_output = f"{arg_input.removesuffix(arg_input.split('.')[-1])}py"
    
    print(f'comments: {len(inter.comments)}')
    print(f'functions: {len(inter.functions)}')
    print(f'classes: {len(inter.classes)}')
    # print(f'conditionals: {len(inter.conditionals)}')

    with open(arg_output, 'w') as out_file:
        out_file.write(inter.parse())

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