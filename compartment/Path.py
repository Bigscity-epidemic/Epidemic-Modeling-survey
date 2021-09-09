ERRCODE = {
    'SUCCEED': 0,
    'DUPLICATED_PARAMETER_NAME': 8,
    'BOTH_SINGLE_AND_EMBEDDING': 9,
    'NOT_SINGLE_NOR_EMBEDDING': 10
}


class Path:
    pre_name = ''
    next_name = ''
    expression = ''
    name2parameters = {}

    def __init__(self, pre_name: str, next_name: str):
        self.pre_name = pre_name
        self.next_name = next_name

    def set_exp(self, exp: str):
        self.expression = exp
        return ERRCODE['SUCCEED']

    def set_parameters(self, name: str, parameter: float = None, embedding: list = None):
        if name in self.name2parameters.keys():
            return ERRCODE['DUPLICATED_PARAMETER_NAME']
        if parameter is None and embedding is None:
            return ERRCODE['NOT_SINGLE_NOR_EMBEDDING']
        if parameter is None:
            self.name2parameters[name] = ['embedding', embedding]
            return ERRCODE['SUCCEED']
        elif embedding is None:
            self.name2parameters[name] = ['single', parameter]
            return ERRCODE['SUCCEED']
        else:
            return ERRCODE['BOTH_SINGLE_AND_EMBEDDING']
