from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Descriptor import vertical_divide, horizontal_divide, add_path
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model


class ExeUI:
    model = None
    graph = None

    def __init__(self):
        self.model = None
        self.graph = None

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
        return result

    def send_message(self, message: dict):
        handle = message['handle']
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
                return [r, self.model, self.get_all_params(self.model)]
            else:
                r = set_path_parameters(self.model, message['src'], message['dst'], message['name'], parameter=None,
                                        embedding=value)
                return [r, self.model, self.get_all_params(self.model)]


if __name__ == '__main__':
    exe = ExeUI()
    exe.send_message({'handle': 'init', 'init_name': 'S'})
    exe.send_message({'handle': 'subdivide', 'type': 'ver', 'origin': 'S', 'new': ['E', 'P', 'I', 'R']})
    exe.send_message({'handle': 'subdivide', 'type': 'hor', 'origin': 'I', 'new': ['A']})
    exe.send_message({'handle': 'subdivide', 'type': 'ver', 'origin': 'I', 'new': ['Is']})
    exe.send_message({'handle': 'subdivide', 'type': 'hor', 'origin': 'Is', 'new': ['Is_ct']})
    graph_finish = exe.send_message({'handle': 'subdivide', 'type': 'add', 'origin': 'E', 'new': 'Is'})

    r1 = exe.send_message({'handle': 'formula', 'src': 'E', 'dst': 'P', 'exp': 'gamma*E*nocontact'})
    print(r1)
    r2 = exe.send_message({'handle': 'param', 'src': 'E', 'dst': 'P', 'name': 'gamma', 'value': 0.5})
    print(r2)
    r3 = exe.send_message({'handle': 'param', 'src': 'E', 'dst': 'P', 'name': 'nocontact', 'value': [0.5, 0.4]})
    print(r3)
