import sys

class Error:
    def __init__(self, text, kind, line):
        self.text = text
        self.kind = kind
        self.line = line
        if type(self.text) != list:
            if '\n' in self.text:
                self.text = [t for t in self.text.split('\n')]
            else:
                self.text = [self.text]
    
    def __str__(self):
        return self.text

    def print_err(self):
        error = '[\033[91mERROR\033[0m]'
        line_prefix = f'\n{error}\t\t'
        txt = line_prefix + line_prefix.join(self.text)
        print(f'{error}\t{self.kind} Error on line {self.line}:{txt}')
        sys.exit(3)

class VariableError(Error):
    def __init__(self, line, text):
        super().__init__(text, 'Variable', line)
    
class RelationError(Error):
    def __init__(self, line, text):
        super().__init__(text, 'Relation', line)
    
class KeywordError(Error):
    def __init__(self, line, text):
        super().__init__(text, 'Keyword', line)

class SyntaxError(Error):
    def __init__(self, line, text):
        super().__init__(text, 'Syntax', line)