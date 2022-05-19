class Block:
    def __init__(self, name, params, instructions, condition, kind):
        self.name = name
        self.params = params
        self.instructions = instructions
        self.condition = condition
        self.kind = kind

class Conditional_Block(Block):
    def __init__(self, instructions, condition):
        super().__init__('Conditional', None, instructions, condition, 'Condition')

class Function_Block(Block):
    def __init__(self, name, params, instructions):
        super().__init__(name, params, instructions, None, 'Function')

    def __str__(self):
        return f'Name: {self.name}\nParams: {", ".join(self.params)}\nInstructions: {len(self.instructions)}'

# Not sure if it will be implemented
class Class_Block(Block):
    def __init__(self, name, functions):
        super().__init__(name, None, functions, None, 'Class')
