from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide, horizontal_divide, add_path
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values

graph = Graph('basic_SEIR', 'S1')
poi_nums = 5
meta = []
for i in range(2, poi_nums + 1):
    meta.append('S' + str(i))
print(horizontal_divide(graph, 'S1', meta))
for i in range(1, poi_nums + 1):
    vertical_divide(graph, 'S' + str(i), ['I' + str(i), 'R' + str(i)])
for i in range(1, poi_nums + 1):
    for j in range(1, poi_nums + 1):
        for cpm in ['S', 'I', 'R']:
            if i != j:
                add_path(graph, cpm + str(i), cpm + str(j))
model = Model('meta', graph)

visual_model(model)
