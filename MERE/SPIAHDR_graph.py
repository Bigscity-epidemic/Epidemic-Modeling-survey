from compartment.Descriptor import vertical_divide, horizontal_divide, add_path
from compartment.Graph import Graph
from compartment.Model import Model
from visual.visual_graph import visual_model


def get_eqs():
    graph = Graph('SPIAHDR', 'S')
    vertical_divide(graph, 'S', ['P', 'I'])
    horizontal_divide(graph, 'I', ['A'])
    vertical_divide(graph, 'I', ['R'])
    horizontal_divide(graph, 'R', ['H'])
    vertical_divide(graph, 'H', ['Icu', 'D'])
    add_path(graph, 'A', 'R')
    add_path(graph, 'H', 'R')
    add_path(graph, 'Icu', 'H')
    model = Model('SEIR_eqs', graph)
    visual_model(model)
    return model


if __name__ == '__main__':
    model = get_eqs()
    visual_model(model)


