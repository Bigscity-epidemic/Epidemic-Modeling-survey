from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide, horizontal_divide
from compartment.Transfer import init_compartment, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values

graph = Graph('SUEIR', 'S')
print(vertical_divide(graph, 'S', ['E', 'I', 'R']))
print(horizontal_divide(graph, 'I', ['U', 'IS']))
model = Model('SEEUIRR', graph)
visual_model(model)
print(set_path_parameters(model, 'S', 'E', False, 0.001))
print(set_path_parameters(model, 'E', 'I', False, 0.001))
print(set_path_parameters(model, 'E', 'U', False, 0.002))
print(set_path_parameters(model, 'E', 'IS', False, 0.003))
print(set_path_parameters(model, 'I', 'R', False, 0.5))
print(set_path_parameters(model, 'U', 'R', False, 0.3))
print(set_path_parameters(model, 'IS', 'R', False, 0.1))
init_value = {'S': 10000.0, 'E': 100.0, 'I': 100.0, 'U': 200.0, 'IS': 300.0, 'R': 0.0}
print(init_compartment(model, init_value))
visual_compartment_values(model)
executor = Executor(model)
for index in range(10):
    executor.simulate_step(index)
visual_compartment_values(model)
