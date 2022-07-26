from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Descriptor import vertical_divide
from compartment.Transfer import set_path_exp, set_path_parameters

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
