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
            name = name.split('(')[0].strip()
            name = name.replace(' ', '_')

            params = current_line.split('(')[1].split(')')[0]
            params = params.split(',')

            instructions = []
            depth = 0
            for line in self.lines[pointer + 1:]:
                if '{' in line:
                    depth += 1
                if '}' in line:
                    depth -= 1
                if depth < 0:
                    break
                instructions.append(line)
            
            self.functions[name] = Function_Block(name, params, instructions)