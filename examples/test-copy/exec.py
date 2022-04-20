from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values

graph = Graph('basic_SEIR', 'S')
vertical_divide(graph, 'S', ['E', 'I', 'R'])
model = Model('basic_SEIR', graph)

beta = 0.5
alpha = 0.1
gamma = 0.1
population = 10000
set_path_exp(model, 'S', 'E', 'beta*S*I*popu')
set_path_parameters(model, 'S', 'E', 'beta', beta)
set_path_parameters(model, 'S', 'E', 'popu', 1.0 / population)
set_path_exp(model, 'E', 'I', 'alpha*E')
set_path_parameters(model, 'E', 'I', 'alpha', alpha)
set_path_exp(model, 'I', 'R', 'gamma*I')
set_path_parameters(model, 'I', 'R', 'gamma', gamma)

init_value = {'S': 9995, 'E': 2, 'I': 3, 'R': 0}
init_compartment(model, init_value)
executor = Executor(model)
for index in range(5):
    executor.simulate_step(index)
    print('_______________________________________')
    print('day {}'.format(index + 1))
    visual_compartment_values(model)
