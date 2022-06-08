import sys

class Error:
    def __init__(self, text, kind, line):
        self.text = text
        self.kind = kind
        self.line = line
    
    def __str__(self, text):
        return self.text

    def print_err(self):
        print(f'{self.kind}Error on line {self.line}:\n\t{self.text}')
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