class Block:
    def __init__(self, name, params, instructions, condition, kind, depth):
        self.name = name
        self.params = [param.strip() for param in params]
        self.instructions = [ins.strip() for ins in instructions]
        self.condition = condition
        self.kind = kind
        self.depth = depth
        self.functions = []
        self.classes = []
        self.conditionals = []
    
    def append_nested_blocks(self, functions, classes, conditionals):
        self.functions = functions
        self.classes = classes
        self.conditionals = conditionals
    
    def parse(self):
        indents = (self.depth + 1) * '\t'
        ins = f'\n{indents}'.join(self.instructions)
        ins = ins.replace('{', '').replace('}', '')
        params = ', '.join(self.params)
        funcs = f'\n{indents}'.join([self.functions[func].parse() for func in self.functions])

        match(self.kind):
            case 'Function':
                return f'def {self.name} ({params}):\n\t{ins}'
            
            case 'Class':
                return f'class {self.name}:\n\t{ins}'

class Conditional_Block(Block):
    def __init__(self, instructions, condition, follow_up_conditionals, depth):
        super().__init__('If', None, instructions, condition, 'Condition', depth)
        self.follow_up_conditionals = follow_up_conditionals

class Follow_Up_Conditional_Block(Conditional_Block):
    def __init__(self, instructions, condition):
        super().__init__(instructions, condition)

class Function_Block(Block):
    def __init__(self, name, params, instructions, depth):
        super().__init__(name, params, instructions, None, 'Function', depth)

    def __str__(self):
        return f'Name: {self.name}\nParams: {", ".join(self.params)}\nInstructions: {len(self.instructions)}'

# Not sure if it will be implemented
class Class_Block(Block):
    def __init__(self, name, functions):
        super().__init__(name, None, functions, None, 'Class', 0)
