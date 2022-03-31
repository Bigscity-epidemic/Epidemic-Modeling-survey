from compartment.Descriptor import vertical_divide, horizontal_divide, add_path
from compartment.Graph import Graph
from compartment.Model import Model
from visual.visual_graph import visual_model


def get_eqs():
    graph = Graph('SEPIIsR', 'S')
    vertical_divide(graph, 'S', ['E', 'P', 'I', 'R'])
    horizontal_divide(graph, 'I', ['A'])
    vertical_divide(graph, 'I', ['Is'])
    horizontal_divide(graph, 'Is', ['Is_ct'])
    graph.add_single_node('Income')
    add_path(graph, 'E', 'Is')
    add_path(graph, 'Income', 'I')
    add_path(graph, 'P', 'Is')
    model = Model('SEIR_eqs', graph)
    visual_model(model)
    return model


if __name__ == '__main__':
    model = get_eqs()
