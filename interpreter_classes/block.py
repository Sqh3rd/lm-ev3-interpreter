class Block:
    def __init__(self, name, params, instructions, condition, kind, depth, line_of_decleration, inter, c_depth):
        self.name = name
        self.params = [param.strip() for param in params] if params else []
        self.instructions = [ins.strip() for ins in instructions]
        self.condition = condition
        self.kind = kind
        self.depth = depth
        self.line_of_decleration = line_of_decleration

        temp_ins = []
        for ins in self.instructions:
            t = ins
            if '{' in ins:
                if c_depth == 0:
                    t = t.replace('{', '')
                c_depth += 1
            if '}' in ins:
                c_depth -= 1
                if c_depth == 0:
                    t = t.replace('}', '')
            t = t.strip()
            if t:
                temp_ins.append(t)

        self.instructions = temp_ins

        if not self.instructions:
            self.instructions = [f'# empty {self.kind}', 'pass']

        self.functions = []
        self.classes = []
        self.conditionals = []

    def parse(self):
        indents = (self.depth + 1) * '\t'
        indents = f'\n{indents}'
        ins = indents + indents.join(self.instructions)
        params = ', '.join(self.params)
        funcs = f'\n{indents}'.join([self.functions[func].parse() for func in self.functions])

        key_word_indents = self.depth * '\t'
        match(self.kind):
            case 'Function':
                return f'\n{key_word_indents}def {self.name} ({params}):{ins}'
            
            case 'Class':
                return f'\n{key_word_indents}class {self.name}:{funcs}{ins}'

class Conditional_Block(Block):
    def __init__(self, instructions, condition, follow_up_conditionals, depth, line_of_decleration, inter, c_depth):
        super().__init__('If', None, instructions, condition, 'Condition', depth, line_of_decleration, inter, c_depth)
        self.follow_up_conditionals = follow_up_conditionals

class Follow_Up_Conditional_Block(Conditional_Block):
    def __init__(self, instructions, condition, line_of_decleration):
        super().__init__(instructions, condition)

class Function_Block(Block):
    def __init__(self, name, params, instructions, depth, line_of_decleration, inter, c_depth):
        super().__init__(name, params, instructions, None, 'Function', depth, line_of_decleration, inter, c_depth)

    def append_nested_blocks(self, conditionals):
        self.conditionals.append(conditionals)

    def __str__(self):
        return f'Name: {self.name}\nParams: {", ".join(self.params)}\nInstructions: {len(self.instructions)}'

# Not sure if it will be implemented
class Class_Block(Block):
    def __init__(self, name, instructions, depth, line_of_decleration, inter, c_depth):
        super().__init__(name, None, instructions, None, 'Class', depth, line_of_decleration, inter, c_depth)

    def append_nested_blocks(self, functions, conditionals):
        self.functions.append(functions)
        self.conditionals.append(conditionals)