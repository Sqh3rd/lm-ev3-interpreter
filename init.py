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
    
    print(f'input: {arg_input}')
    print(f'output: {arg_output}')
    comments = "\n".join([str(c) for c in inter.comments])
    print(f'comments:\n{comments}')

if __name__ == "__main__":
    parse_args(sys.argv)