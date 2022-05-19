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

    def read_file(self, path):
        with open(path, 'r') as f:
            for l in f:
                self.lines.append(l)
    
    def sort_lines(self):
        for i, line in enumerate(self.lines):
            line_number = i + 1

            if 'func' in line:
                add_func_pointer = True
                if self.comment_identifier in line and 'func' in line.split(self.comment_identifier)[1]:
                    add_func_pointer = False
                if add_func_pointer:
                    self.function_pointer.append(i)

            elif 'class' in line:
                add_class_pointer = True
                if self.comment_identifier in line and 'class' in line.split(self.comment_identifier)[1]:
                    add_class_pointer = False
                if add_class_pointer:
                    self.class_pointer.append(i)
            
            if self.comment_identifier in line:
                c = line.split(self.comment_identifier)[1].strip()
                if c:
                    self.comments.append(Comment(line_number, c, self.comment_identifier))
                else:
                    self.comments.append(Empty_Comment(line_number))
    
    def create_functions(self, function_pointers):
        for pointer in function_pointers:
            current_line = self.lines[pointer]

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

            for line in self.lines[pointer:]:
                if '{' in line:
                    depth += 1
                if '}' in line:
                    depth -= 1
                if line != current_line:
                    instructions.append(line)
                if depth == 0:
                    function_is_concluded = True
                    break
            
            if not function_is_concluded:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\tFunction \'{name}\' is never concluded!')
            self.functions[name] = Function_Block(name, params, instructions)
    
    def create_classes(self, class_pointers):
        for pointer in class_pointers:
            current_line = self.lines[pointer]

            name = current_line.removeprefix('class')
            depth = 0
            if '{' in name:
                depth = 1
                name = name.split('{')[0]
            name = name.strip()

            class_is_concluded = False

            functions = []

            for line in self.lines[pointer + 1]:
                if '{' in line:
                    depth += 1
                if '}' in line:
                    depth -= 1
                if 'func' in line:
                    f_name = current_line.removeprefix('func')
                    f_name = f_name.split('(')[0].strip()
                    f_name = f_name.replace(' ', '_')
                    functions.append(self.functions[f_name])
                if depth == 0:
                    class_is_concluded = True
                    break

            if not class_is_concluded:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\Class \'{name}\' is never concluded!')

            self.classes[name] = Class_Block(name, functions)