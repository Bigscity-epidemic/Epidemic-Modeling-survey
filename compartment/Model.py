from compartment.Compartment import Compartment
from compartment.Path import Path
from compartment.Graph import Graph

ERRCODE = {
    'SUCCEED': 0,
    'COMPARTMENT_NAME_NOT_FOUND': 6,
    'PATH_NAME_NOT_FOUND': 7
}


class Model:
    name = ''
    name2compartments = {}
    name2paths = {}

    def __init__(self, name: str, graph: Graph):
        self.name = name
        for node_name in graph.name2node.keys():
            compartment = Compartment(graph.name2node[node_name], 0.0)
            self.name2compartments[node_name] = compartment
        for compartment_name in self.name2compartments.keys():
            pre_name = compartment_name
            for next_name in self.name2compartments[compartment_name].node.next_name_list.keys():
                path = Path(pre_name, next_name)
                path_name = pre_name + '->' + next_name
                self.name2paths[path_name] = path

    def set_compartment(self, name: str, value: float):
        if name not in self.name2compartments.keys():
            return ERRCODE['COMPARTMENT_NAME_NOT_FOUND']
        self.name2compartments[name].value = value
        return ERRCODE['SUCCEED']

    def set_path_exp(self, pre_name: str, next_name: str, exp: str):
        if pre_name not in self.name2compartments.keys() or next_name not in self.name2compartments.keys():
            return ERRCODE['COMPARTMENT_NAME_NOT_FOUND']
        path_name = pre_name + '->' + next_name
        if path_name not in self.name2paths.keys():
            return ERRCODE['PATH_NAME_NOT_FOUND']
        path = self.name2paths[path_name]
        return path.set_exp(exp)

    def set_path_parameters(self, pre_name: str, next_name: str, parameter_name: str, parameter: float = None,
                            embedding: list = None):
        if pre_name not in self.name2compartments.keys() or next_name not in self.name2compartments.keys():
            return ERRCODE['COMPARTMENT_NAME_NOT_FOUND']
        path_name = pre_name + '->' + next_name
        if path_name not in self.name2paths.keys():
            return ERRCODE['PATH_NAME_NOT_FOUND']
        path = self.name2paths[path_name]
        return path.set_parameters(parameter_name, parameter, embedding)
