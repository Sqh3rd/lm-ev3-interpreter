from .exceptions import VariableError, RelationError

class Condition:
    def __init__(self, variables, relations):
        self.variables = variables
        self.relations = relations
    
    def evaluate(self, allowed_variables, allowed_relations):
        for var in self.variables:
            if var not in allowed_variables:
                raise VariableError(f'{var} doesn\'t exist!')
        for rel in self.relations:
            if rel not in allowed_relations:
                raise RelationError(f'The \'{rel}\' operator is not allowed!')