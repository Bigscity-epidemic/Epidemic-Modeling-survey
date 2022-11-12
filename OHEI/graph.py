from compartment.Descriptor import vertical_divide, horizontal_divide, add_path
from compartment.Graph import Graph
from compartment.Model import Model
from visual.visual_graph import visual_model


def get_eqs():
    graph = Graph('CovidM', 'S')
    horizontal_divide(graph, 'S', ['V'])
    vertical_divide(graph, 'S', ['E','Ip', 'Ic', 'R'])
    vertical_divide(graph, 'V', ['Ev', 'Is'])
    add_path(graph, 'S', 'V')
    add_path(graph, 'V', 'S')
    add_path(graph, 'V', 'E')
    add_path(graph, 'R', 'S')
    add_path(graph, 'E', 'Is')
    add_path(graph, 'Is', 'R')

    model = Model('OHEI', graph)
    return model


if __name__ == '__main__':
    model = get_eqs()
    visual_model(model)
