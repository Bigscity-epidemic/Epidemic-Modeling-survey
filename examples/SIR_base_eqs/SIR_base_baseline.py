from compartment.Descriptor import vertical_divide
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment
from executor.Executor import Executor
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line
from matplotlib import pyplot as plt
from matplotlib.font_manager import *
from math import log

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.font_manager import *

myfont = FontProperties(fname='simhei.ttf', size=14)


def get_SIR_base_eqs(INPUT, beta, gamma):
    graph = Graph('SIR_base_eqs', 'S')
    vertical_divide(graph, 'S', ['I', 'R'])
    model = Model('SIR_base_eqs', graph)
    S = INPUT[0]
    I = INPUT[1]
    R = INPUT[2]
    population = S + I + R
    set_path_exp(model, 'S', 'I', 'beta*S*I')
    set_path_parameters(model, 'S', 'I', 'beta', beta / population)
    set_path_exp(model, 'I', 'R', 'gamma*I')
    set_path_parameters(model, 'I', 'R', 'gamma', gamma)
    init_value = {'S': S, 'I': I, 'R': R}
    init_compartment(model, init_value)
    return model


if __name__ == '__main__':
    days = 10
    S = 51580000
    I = 60000
    R = 40000
    population = S + I + R
    INPUT = [S, I, R]
    beta = 0.35
    gamma = 0.2
    model = get_SIR_base_eqs(INPUT, beta, gamma)
    visual_compartment_values(model)
    executor = Executor(model)
    values = model.get_values()
    for name in values.keys():
        values[name] = [values[name]]
    for index in range(days):
        executor.simulate_step(index)
        tmp_value = model.get_values()
        for name in values.keys():
            values[name].append(tmp_value[name])
    visual_compartment_values(model)
    print(values)
