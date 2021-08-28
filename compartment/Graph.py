from compartment.Node import Node

ERRCODE = {
    'SUCCEED': 0,
    'NODE_NAME_NOT_FOUND': 1,
    'DUPLICATED_NAME': 2,
    'NO_SELF_CIRCLE': 3
}


class Graph:
    name = ''
    name2node = {}

    def __init__(self, model_name:str, init_compartment_name:str):
        self.name = model_name
        init_node = Node(init_compartment_name)
        self.name2node[init_compartment_name] = init_node

    def add_single_node(self,node_name:str):
        if node_name in self.name2node.keys():
            return ERRCODE['DUPLICATED_NAME']
        new_node = Node(node_name)
        self.name2node[node_name] = new_node
        return ERRCODE['SUCCEED']

    def add_next(self, pre_node_name:str, new_node_name:str):
        if pre_node_name not in self.name2node.keys():
            return ERRCODE['NODE_NAME_NOT_FOUND']
        if new_node_name in self.name2node.keys():
            return ERRCODE['DUPLICATED_NAME']
        self.name2node[pre_node_name].add_next(new_node_name)
        new_node = Node(new_node_name)
        self.name2node[new_node_name] = new_node
        return ERRCODE['SUCCEED']

    def add_edge(self, from_name:str, to_name:str):
        if from_name not in self.name2node.keys() or to_name not in self.name2node.keys():
            return ERRCODE['NODE_NAME_NOT_FOUND']
        if from_name == to_name:
            return ERRCODE['NO_SELF_CIRCLE']
        return self.name2node[from_name].add_next(to_name)
