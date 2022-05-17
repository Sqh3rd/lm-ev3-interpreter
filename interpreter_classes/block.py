class Block:
    def __init__(self, name, params, instructions, condition, kind):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.condition = condition
        self.kind = kind

class Function_Block(Block):
    def __init__(self, name, params, instructions):
        super().__init__(name, params, instructions, None, 'Function')

    def __str__(self):
        return f'Name: {self.name}\nParams: {", ".join(self.params)}\nInstructions: {len(self.instructions)}'

class Class_Block(Block):
    def __init__(self, name, instructions):
        super().__init__(name, None, instructions, None, 'Class')