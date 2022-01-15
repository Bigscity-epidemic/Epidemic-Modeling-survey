from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from math import log10
from matplotlib import pyplot as plt
from visual.visual_value_line import plot_line
from utils.get_logindex import get_logindex

graph = Graph('basic_SEIR', 'S')
print(vertical_divide(graph, 'S', ['E', 'I', 'R']))
model = Model('basic_SEIR', graph)
population = 1000000.0
init_infectious = 22.0
init_exposed = 30.0
init_removed = 34.0
init_confirmed = 15.0
days = 100
beta = []
for i in range(100):
    beta.append(0.45 / population)
beta[27] = 0.5 / population
print(set_path_exp(model, 'S', 'E', 'beta*S*I'))
print(set_path_parameters(model, 'S', 'E', 'beta', embedding=beta))
print(set_path_exp(model, 'E', 'I', 'sigma*E'))
print(set_path_parameters(model, 'E', 'I', 'sigma', 1.0 / 4.6))
print(set_path_exp(model, 'I', 'R', 'gamma*I'))
print(set_path_parameters(model, 'I', 'R', 'gamma', 1.0 / 5.0))
init_value = {'S': population - init_exposed - init_infectious - init_removed, 'E': init_exposed, 'I': init_infectious,
              'R': init_removed}
print(init_compartment(model, init_value))
executor = Executor(model)
values = model.get_values()
for name in values.keys():
    values[name] = [values[name]]
for index in range(days):
    executor.simulate_step(index)
    tmp_value = model.get_values()
    for name in values.keys():
        values[name].append(tmp_value[name])
comfirm_pred = [15.0]
for i in range(100):
    comfirm_pred.append(comfirm_pred[-1] + values['I'][i] / 14.0)
values['C'] = comfirm_pred
plot_line(values,log=True)

lambdac = get_logindex(values['C'])[0:60]
lambdai = get_logindex(values['I'])[0:60]

lambda_value = {'C': lambdac, 'I': lambdai}
plot_line(lambda_value)
