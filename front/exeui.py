from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Descriptor import vertical_divide, horizontal_divide, add_path
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters, reset_parameters
from visual.visual_graph import visual_model
from executor.Executor import Executor


class ExeUI:
    model = None
    graph = None
    init_value = {}

    def __init__(self):
        self.model = None
        self.graph = None
        self.init_value = {}

    def get_all_params(self, model: Model):
        result = {}
        for pathname in model.name2paths.keys():
            path = model.name2paths[pathname]
            param2value = {}
            exp = path.expression
            if exp == '':
                result[pathname] = {}
                continue
            exp = exp.replace('+', '*').split('*')
            for variable in exp:
                if not variable[0].isupper():
                    param2value[variable] = None
            for paramname in path.name2parameters.keys():
                param2value[paramname] = path.name2parameters[paramname][1]
            result[pathname] = param2value
        for compartment in self.init_value.keys():
            result[compartment] = self.init_value[compartment]
        return result

    def send_message(self, message: dict):
        handle = message['handle']
        if handle == 'run':
            init_compartment(self.model, self.init_value)
            executor = Executor(self.model)
            executor.simulate_step(1)
            self.init_value = self.model.get_values()
            return [self.model, self.get_all_params(self.model)]
        if handle == 'init':
            self.graph = Graph('your graph', message['init_name'])
            self.model = Model('your model', self.graph)
            return [0, self.model, {}]

        if handle == 'subdivide':
            if message['type'] == 'ver':
                method = vertical_divide
            elif message['type'] == 'hor':
                method = horizontal_divide
            else:
                method = add_path
            r = method(self.graph, message['origin'], message['new'])
            if r != 0:
                return [r, self.model, {}]
            self.model = Model('your model', self.graph)
            return [0, self.model, {}]

        if handle == 'formula':
            r = set_path_exp(self.model, message['src'], message['dst'], message['exp'])
            return [r, self.model, self.get_all_params(self.model)]

        if handle == 'param':
            value = message['value']
            if type(value) == float:
                r = set_path_parameters(self.model, message['src'], message['dst'], message['name'], value)
                if r != 0:
                    r = reset_parameters(self.model, message['name'], value)
                return [r, self.model, self.get_all_params(self.model)]
            else:
                r = set_path_parameters(self.model, message['src'], message['dst'], message['name'], parameter=None,
                                        embedding=value)
                return [r, self.model, self.get_all_params(self.model)]

        if handle == 'setvalue':
            self.init_value[message['compartment']] = message['value']
            return [0, self.model, self.get_all_params(self.model)]


if __name__ == '__main__':
    exe = ExeUI()

    exe.send_message({'handle': 'init', 'init_name': 'S'})
    exe.send_message({'handle': 'subdivide', 'type': 'ver', 'origin': 'S', 'new': ['I', 'R']})

    exe.send_message({'handle': 'formula', 'src': 'S', 'dst': 'I', 'exp': 'beta*S*I*popu'})
    exe.send_message({'handle': 'param', 'src': 'S', 'dst': 'I', 'name': 'beta', 'value': 0.3})
    exe.send_message({'handle': 'param', 'src': 'S', 'dst': 'I', 'name': 'popu', 'value': 0.00001})

    exe.send_message({'handle': 'formula', 'src': 'I', 'dst': 'R', 'exp': 'gamma*I'})
    exe.send_message({'handle': 'param', 'src': 'I', 'dst': 'R', 'name': 'gamma', 'value': 0.1})

    exe.send_message({'handle': 'setvalue', 'compartment': 'S', 'value': 99990})
    exe.send_message({'handle': 'setvalue', 'compartment': 'I', 'value': 10})
    exe.send_message({'handle': 'setvalue', 'compartment': 'R', 'value': 0})

    model, p = exe.send_message(message={'handle': 'run'})
    print(p, model.get_values())
