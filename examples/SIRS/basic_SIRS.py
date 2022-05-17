from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide, add_path
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values

graph = Graph('basic_SIRS', 'S')
print(vertical_divide(graph, 'S', ['I','R']))
print(add_path(graph,'R','S'))
model = Model('basic_SIRS', graph)
visual_model(model)
population = 10000.0
init_infectious = 10.0
beta = 0.4
gamma = 0.2
theta = 0.1
print(set_path_exp(model, 'S', 'I', 'beta*S*I'))
print(set_path_parameters(model, 'S', 'I', 'beta', beta / population))
print(set_path_exp(model, 'I', 'R', 'gamma*I'))
print(set_path_parameters(model, 'I', 'R', 'gamma', gamma))
print(set_path_exp(model, 'R', 'S', 'theta*R'))
print(set_path_parameters(model, 'R', 'S', 'theta', theta))
init_value = {'S': population - init_infectious,  'I': init_infectious, 'R':0}
print(init_compartment(model, init_value))
visual_compartment_values(model)
executor = Executor(model)
for index in range(360):
    executor.simulate_step(index)
visual_compartment_values(model)
