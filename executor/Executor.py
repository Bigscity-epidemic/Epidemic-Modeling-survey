from compartment.Model import Model


class Executor:
    model = None

    def __init__(self, model: Model):
        self.model = model

    def simulate_step(self, index: int):
        path2value = {}
        for pathname in self.model.name2paths.keys():
            pre_name = pathname.split('-')[0]
            path = self.model.name2paths[pathname]
            if path.use_embedding:
                parameter = path.embedding_parameters[index]
            else:
                parameter = path.basic_parameter
            value = parameter * self.model.name2compartments[pre_name].value
            self.model.name2compartments[pre_name].value -= value
            path2value[pathname] = value
        for pathname in path2value.keys():
            next_name = pathname.split('>')[1]
            self.model.name2compartments[next_name].value += path2value[pathname]
