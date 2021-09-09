from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values

graph = Graph('basic_SEIR', 'S')
print(vertical_divide(graph, 'S', ['E', 'I', 'R']))
model = Model('basic_SEIR', graph)
visual_model(model)
population = 10000.0
init_infectious = 10.0
print(set_path_exp(model, 'S', 'E', 'beta*S*I'))
print(set_path_parameters(model, 'S', 'E', 'beta', 0.5 / population))
print(set_path_exp(model, 'E', 'I', 'alpha*E'))
print(set_path_parameters(model, 'E', 'I', 'alpha', 0.1))
print(set_path_exp(model, 'I', 'R', 'gamma*I'))
print(set_path_parameters(model, 'I', 'R', 'gamma', 0.5))
init_value = {'S': population, 'E': 2 * init_infectious, 'I': init_infectious, 'R': 0.0}
print(init_compartment(model, init_value))
visual_compartment_values(model)
executor = Executor(model)
for index in range(360):
    executor.simulate_step(index)
visual_compartment_values(model)
