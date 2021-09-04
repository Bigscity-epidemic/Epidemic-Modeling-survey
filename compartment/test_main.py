from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Descriptor import vertical_divide, horizontal_divide
from compartment.Transfer import init_compartment
from visual.visual_graph import visual_graph, visual_model

graph = Graph('SUEIR', 'S')
print(vertical_divide(graph, 'S', ['E1', 'I', 'R1']))
print(horizontal_divide(graph, 'I', ['U', 'IS']))
print(horizontal_divide(graph, 'E1', ['E2']))
print(horizontal_divide(graph, 'R1', ['R2']))
model = Model('SEEUIRR', graph)
visual_model(model)
init_value = {'S': 10000, 'E1': 100, 'E2': 50, 'I': 100, 'U': 200, 'IS': 300, 'R1': 0, 'R2': 0}
print(init_compartment(model,init_value))
