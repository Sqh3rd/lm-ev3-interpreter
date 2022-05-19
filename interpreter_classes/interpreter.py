from msilib.schema import Class
from .comment import Comment, Empty_Comment
from .block import Function_Block, Class_Block

class Interpreter:
    def __init__(self):
        # Will maybe be customizable
        self.comment_identifier = '//'

        # Lines taken from the code
        self.lines = []
        self.instructions = []
        self.comments = []

        # Objects taken from the code
        self.functions = {}
        self.variables = {}
        self.classes = {}

        # Pointers to lines from the code
        self.function_pointer = []
        self.class_pointer = []
        self.conditional_pointer = []

    def read_file(self, path):
        with open(path, 'r') as f:
            for l in f:
                self.lines.append(l)
    
    def sort_lines(self):
        for i, line in enumerate(self.lines):
            line_number = i + 1

            if 'func' in line and not (self.comment_identifier in line and 'func' in line.split(self.comment_identifier)[1]):
                self.function_pointer.append(i)

            elif 'class' in line and not (self.comment_identifier in line and 'class' in line.split(self.comment_identifier)[1]):
                self.class_pointer.append(i)
            
            elif 'if' in line and not (self.comment_identifier in line and 'if' in line.split(self.comment_identifier)[1]):
                self.conditional_pointer.append(i)

            if self.comment_identifier in line:
                com = line.split(self.comment_identifier)[1].strip()
                if com:
                    self.comments.append(Comment(line_number, com, self.comment_identifier))
                else:
                    self.comments.append(Empty_Comment(line_number))
    
    def create_functions(function_pointers, lines):
        functions = {}
        for pointer in function_pointers:
            current_line = lines[pointer]

            name = current_line.removeprefix('func')
            if not '(' in name:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\t\'(\' expected after function name!')
            name = name.split('(')[0].strip()
            name = name.replace(' ', '_')

            if not ')' in current_line:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\t\')\' expected after function parameters!')
            params = current_line.split('(')[1].split(')')[0]
            params = params.split(',')

            instructions = []
            depth = 0
            if '{' in current_line:
                depth = 1

            function_is_concluded = False

            for line in lines[pointer + 1:]:
                if '{' in line:
                    depth += 1
                if '}' in line:
                    depth -= 1
                instructions.append(line)
                if depth == 0:
                    function_is_concluded = True
                    break
            
            if not function_is_concluded:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\tFunction \'{name}\' is never concluded!')
            functions[name] = Function_Block(name, params, instructions)
        return functions

    def create_classes(class_pointers, lines, functions):
        classes = {}
        for pointer in class_pointers:
            current_line = lines[pointer]

            name = current_line.removeprefix('class')
            depth = 0
            if '{' in name:
                depth = 1
                name = name.split('{')[0]
            name = name.strip()

            class_is_concluded = False

            functions = []

            for line in lines[pointer + 1]:
                if '{' in line:
                    depth += 1
                if '}' in line:
                    depth -= 1
                if 'func' in line:
                    f_name = current_line.removeprefix('func')
                    f_name = f_name.split('(')[0].strip()
                    f_name = f_name.replace(' ', '_')
                    functions.append(functions[f_name])
                if depth == 0:
                    class_is_concluded = True
                    break

            if not class_is_concluded:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\Class \'{name}\' is never concluded!')

            classes[name] = Class_Block(name, functions)
        return classes

    # def create_conditionals(conditional_pointer):