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