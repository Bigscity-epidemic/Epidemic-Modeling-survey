from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters, reset_parameters
from visual.visual_value_line import plot_line
import numpy as np
from math import exp, sin, pi
from random import random, randint
import pandas as pd
from matplotlib import pyplot as plt

graph = Graph('basic_SEIR', 'S')
print(vertical_divide(graph, 'S', ['E', 'I', 'R']))
model = Model('basic_SEIR', graph)
population = 1000000.0
init_infectious = 22.0
init_exposed = 30.0
init_removed = 34.0
init_confirmed = 15.0
days = 100
beta = 0.45
sigma = 1.0 / 4.6
gamma = 1.0 / 5.0
betasin = []
for i in range(100):
    sinfactor = sin(i + 100 * random() * 0.2 * 2 * pi)
    histfactor = 0.5 / randint(1, i + 1)
    factor = 4 * sinfactor + 4 * histfactor
    betasin.append(beta + 0.05 * factor)
    if betasin[-1] < 0:
        betasin[-1] = 0
print(set_path_exp(model, 'S', 'E', 'beta'))
print(set_path_parameters(model, 'S', 'E', 'beta', betasin[0]))
print(set_path_exp(model, 'E', 'I', 'sigma'))
print(set_path_parameters(model, 'E', 'I', 'sigma', sigma))
print(set_path_exp(model, 'I', 'R', 'gamma'))
print(set_path_parameters(model, 'I', 'R', 'gamma', gamma))
init_value = {'S': population, 'E': init_exposed, 'I': init_infectious,
              'R': init_removed}
print(init_compartment(model, init_value))

executor = Executor(model)
values = model.get_values()
for name in values.keys():
    values[name] = [values[name]]

for index in range(days):
    betat = np.random.binomial(values['S'][-1], 1 - exp(-1.0 * betasin[index] * values['I'][-1] / population))
    sigmat = np.random.binomial(values['E'][-1], 1 - exp(-1.0 * sigma))
    gammat = np.random.binomial(values['I'][-1], 1 - exp(-1.0 * gamma))
    reset_parameters(model, 'beta', betat)
    reset_parameters(model, 'sigma', sigmat)
    reset_parameters(model, 'gamma', gammat)
    executor.simulate_step(index)
    tmp_value = model.get_values()
    for name in values.keys():
        values[name].append(tmp_value[name])

comfirm_pred = [15.0]
for i in range(100):
    comfirm_pred.append(comfirm_pred[-1] + values['I'][i] / 14.0)
values['C'] = comfirm_pred
#plot_line(values, log=True)
plt.figure()
if True:
    plt.yscale('log')
    plt.plot(values['S'],label='S', color='yellow')
    plt.plot(values['E'], label='E', color='pink')
    plt.plot(values['I'], label='I', color='blue')
    plt.plot(values['R'], label='R', color='red')
    plt.plot(values['C'], label='C', color='black')
# for name in values:
#     plt.plot(values[name], label=name, linestyle = linestyle)
plt.legend()
plt.show()
plot_line({'beta': betasin})
df = pd.DataFrame(values)
df.to_csv("MyResult/SEIR_SDE.csv")

