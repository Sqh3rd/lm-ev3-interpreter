class Interpreter:
    def __init__(self):
        # Will maybe be customizable
        self.comment_identifier = '//'

        # Lines taken from the code
        self.lines = []
        self.temp_lines = []
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
                self.temp_lines.append(l)
    
    def sort_lines(self):
        for i, line in enumerate(self.temp_lines):
            line_number = i + 1
            if 'func' in line:
                self.function_pointer.append(line_number)
            elif 'class' in line:
                self.class_pointer.append(line_number)
            
            if '//' in line:
                c = line.split(self.comment_identifier)[1].strip()
                if c:
                    self.comments.append(Comment(line_number, c, self.comment_identifier))
                else:
                    self.comments.append(Empty_Comment(line_number))

class Comment:
    def __init__(self, line, content, comment_identifier):
        self.line = line
        self.content = content
        self.prefix = comment_identifier
    
    def __str__(self):
        return f'Comment on line {self.line}:\n\t\'{self.prefix} {self.content}\'\n'

class Empty_Comment(Comment):
    def __init__(self, line):
        self.line = line
    
    def __str__(self):
        return f'Empty comment on line {self.line}\n'