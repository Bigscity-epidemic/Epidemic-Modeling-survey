class Path:
    pre_name = ''
    next_name = ''
    use_embedding = False
    basic_parameters = 0.0
    embedding_parameters = []

    def __init__(self, pre_name: str, next_name: str):
        self.pre_name = pre_name
        self.next_name = next_name

    def set_parameters(self, parameters: float):
        self.basic_parameters = parameters

    def set_embedding(self, parameters: list):
        self.use_embedding = True
        self.embedding_parameters = parameters
