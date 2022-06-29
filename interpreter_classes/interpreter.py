from .comment import Comment, Empty_Comment
from .block import Function_Block, Class_Block
from .exceptions import KeywordError, RelationError, VariableError, SyntaxError

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
        self.conditionals = []

        # Pointers to lines from the code
        self.function_pointer = []
        self.class_pointer = []
        self.conditional_pointer = []

    def read_file(self, path):
        with open(path, 'r') as f:
            for l in f:
                self.lines.append(l)
    
    def sort_lines(lines, comment_identifier):
        function_pointer = []
        class_pointer = []
        conditional_pointer = []
        comments = []
        depth = 0
        for i, line in enumerate(lines):
            line_number = i + 1
            stripped_line = line.strip()
            line_split = stripped_line.split(' ')

            if depth == 0:
                if stripped_line.startswith('func ') and not (comment_identifier in stripped_line and 'func' in stripped_line.split(comment_identifier)[1]):
                    func_def_err = KeywordError(line_number, 'Function definitions follow this syntax: func func_name(<args>){ }')
                    if len(line_split) < 2:
                        func_def_err.print_err()
                    elif ('(' in line_split[1] and line_split[1][0] != '(') or (len(line_split) > 2 and '(' in line_split[2]) and ')' in line:
                        function_pointer.append(i)
                    else:
                        if not ')' in line:
                            SyntaxError(line_number, f'\')\' expected after function parameters!').print_err()
                        SyntaxError(line_number, f'\'(\' expected after function name!').print_err

                elif stripped_line.startswith('class ') and not (comment_identifier in line and 'class' in line.split(comment_identifier)[1]):
                    class_def_err = KeywordError(line_number, 'Class definitions follow this syntax: class Class_name { }')
                    if len(line_split) < 2 or not line_split[1].isalpha():
                        class_def_err.print_err()
                    else:
                        class_pointer.append(i)
                
                elif stripped_line.startswith('if') and not (comment_identifier in line and 'if' in line.split(comment_identifier)[1]):
                    conditional_pointer.append(i)

                if comment_identifier in line:
                    com = line.split(comment_identifier)[1].strip()
                    if com:
                        comments.append(Comment(line_number, com, comment_identifier))
                    else:
                        comments.append(Empty_Comment(line_number))
            
            if '{' in line:
                depth += 1
            if '}' in line:
                depth -= 1

        return function_pointer, class_pointer, conditional_pointer, comments
    
    def create_functions(function_pointers, lines):
        functions = {}
        for pointer in function_pointers:
            current_line = lines[pointer]

            name = current_line.strip().removeprefix('func')

            name = name.split('(')[0].strip()
            name = name.replace(' ', '_')

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

    def create_classes(class_pointers, lines):
        classes = {}
        for pointer in class_pointers:
            current_line = lines[pointer]

            name = current_line.strip().removeprefix('class')
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
                if depth == 0:
                    class_is_concluded = True
                    break

            if not class_is_concluded:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\tClass \'{name}\' is never concluded!')

            classes[name] = Class_Block(name, functions)
        return classes

    def create_conditionals(conditional_pointer, lines):
        conditionals = []
        for pointer in conditional_pointer:
            instructions = []

            depth = 0
            conditional_is_concluded = False

            follow_up_pointer = []

            if '{' in lines[pointer]:
                depth = 1
            for i, line in enumerate(lines[pointer + 1:]):
                if '{' in line:
                    depth += 1
                if '}' in line:
                    depth -= 1
                if 'else' in line:
                    follow_up_pointer.append(pointer + 1 + i)
                instructions.append(line)
                if depth == 0:
                    conditional_is_concluded = True
                    break
            
            if not conditional_is_concluded:
                raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\tConditional \'if\' statement is never concluded!')
            
            for pointer in follow_up_pointer:
                follow_up_instructions = []

                follow_up_depth = 0
                follow_up_conditional_is_concluded = False

                name = lines[pointer]

                condition = ''

                if name.replace(' ', '').startswith('}'):
                    name = name.split('}')[1]
                if '(' in name:
                    if not ')' in name:
                        raise SyntaxError(f'SyntaxError on line {pointer+1}:\n\t\')\' expected after condition!')
                    condition = name.split('(')[1].split(')')[0]
                    name = name.split('(')[0]

                if '{' in lines[pointer]:
                    follow_up_depth = 1
                for line in lines[pointer + 1]:
                    if '{' in line:
                        follow_up_depth += 1
                    if '}' in line:
                        follow_up_depth -= 1
                    follow_up_instructions.append(line)
                    if follow_up_depth == 0:
                        follow_up_conditional_is_concluded = True
                        break

                if not follow_up_conditional_is_concluded:
                    raise SyntaxError(f'SyntaxError on line {pointer + 1}:\n\tFollow up Conditional \'{name}\' statement is never concluded!')
    
    def parse(self):
        output = []
        for cl in self.classes:
            output.append(self.classes[cl].parse())
        for fu in self.functions:
            output.append(self.functions[fu].parse())
        return '\n'.join(output)