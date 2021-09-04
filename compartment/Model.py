from compartment.Compartment import Compartment
from compartment.Path import Path
from compartment.Graph import Graph


class Model:
    name = ''
    name2compartments = {}
    pre_name2paths = {}

    def __init__(self, name: str, graph: Graph):
        self.name = name
        for node_name in graph.name2node.keys():
            compartment = Compartment(graph.name2node[node_name], 0.0)
            self.name2compartments[node_name] = compartment
        for compartment_name in self.name2compartments.keys():
            pre_name = compartment_name
            for next_name in self.name2compartments[compartment_name].node.next_name_list.keys():
                path = Path(pre_name, next_name)
                self.pre_name2paths[pre_name] = path
