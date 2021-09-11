from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide, horizontal_divide
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from fit.fit_main import fit_main
import numpy as np

graph = Graph('SEIR', 'S')
print(vertical_divide(graph, 'S', ['E', 'I', 'R']))
model = Model('SEIR', graph)
print(set_path_exp(model, 'S', 'E', 'beta*S*I'))
print(set_path_parameters(model, 'S', 'E', 'beta', 0.00005))
print(set_path_exp(model, 'E', 'I', 'alpha*E'))
print(set_path_parameters(model, 'E', 'I', 'alpha', 0.1))
print(set_path_exp(model, 'I', 'R', 'gamma*I'))
print(set_path_parameters(model, 'I', 'R', 'gamma', 0.5))
init_value = {'S': 10000.0, 'E': 100.0, 'I': 10.0, 'R': 0.0}
print(init_compartment(model, init_value))
visual_compartment_values(model)

confirm_truth = [model.name2compartments['I'].value + model.name2compartments['R'].value]
remove_truth = [model.name2compartments['R'].value]

executor = Executor(model)
for index in range(360):
    executor.simulate_step(index)
    confirm_truth.append(model.name2compartments['I'].value + model.name2compartments['R'].value)
    remove_truth.append(model.name2compartments['R'].value)
visual_compartment_values(model)
fit_main(model, {'I+R': None, 'R': None})
