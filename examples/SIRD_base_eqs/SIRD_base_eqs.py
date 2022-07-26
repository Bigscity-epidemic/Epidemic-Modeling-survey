from compartment.Descriptor import vertical_divide, horizontal_divide
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment
from executor.Executor import Executor
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line
import math


def get_SIRD_base_eqs(INPUT, beta, epsilon, gamma):
    graph = Graph('SEIR_base_eqs', 'S')
    vertical_divide(graph, 'S', ['I', 'R'])
    horizontal_divide(graph, 'R', ['D'])
    model = Model('SIRD_base_eqs', graph)
    S = INPUT[0]
    I = INPUT[1]
    R = INPUT[2]
    D = INPUT[3]
    set_path_exp(model, 'S', 'I', 'beta*S*I')
    set_path_parameters(model, 'S', 'I', 'beta', embedding=beta)
    set_path_exp(model, 'I', 'R', 'epsilon*I')
    set_path_parameters(model, 'I', 'R', 'epsilon', epsilon)
    set_path_exp(model, 'I', 'D', 'gamma*I')
    set_path_parameters(model, 'I', 'D', 'gamma', gamma)
    init_value = {'S': S, 'I': I, 'R': R, 'D': D}
    init_compartment(model, init_value)
    return model


if __name__ == '__main__':
    days = 10
    S = 100000
    I = 50
    R = 0
    D = 0
    population = S + I + R + D
    INPUT = [S, I, R, D]
    beta = 1.5
    beta_seires = []
    for i in range(days):
        beta_seires.append(beta / population * 0.5 * (4.0 - math.log(i + 4)))
    epsilon = 0.2
    gamma = 0.001
    model = get_SIRD_base_eqs(INPUT, beta_seires, epsilon, gamma)
    visual_model(model)
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
        print(index)
        visual_compartment_values(model)
    beta_forplot = []
    for item in beta_seires:
        beta_forplot.append(item * population)
    plot_line({'beta_seires': beta_forplot})
    values_forplot=values.copy()
    values_forplot.pop('S')
    plot_line(values_forplot)
