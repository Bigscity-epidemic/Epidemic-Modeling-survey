from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Descriptor import vertical_divide, horizontal_divide
from visual.visual_graph import visual_graph, visual_model

graph = Graph('SUEIR', 'S')
print(vertical_divide(graph, 'S', ['E1', 'I', 'R1']))
print(horizontal_divide(graph, 'I', ['U', 'IS']))
print(horizontal_divide(graph, 'E1', ['E2']))
print(horizontal_divide(graph, 'R1', ['R2']))
visual_graph(graph)
model = Model('SEEUIRR', graph)
visual_model(model)
