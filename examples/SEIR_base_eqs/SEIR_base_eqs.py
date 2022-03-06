from compartment.Descriptor import vertical_divide
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment
from executor.Executor import Executor
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line


def get_SEIR_base_eqs(INPUT, beta, epsilon, gamma):
    graph = Graph('SEIR_base_eqs', 'S')
    vertical_divide(graph, 'S', ['E', 'I', 'R'])
    model = Model('SEIR_base_eqs', graph)
    S = INPUT[0]
    E = INPUT[1]
    I = INPUT[2]
    R = INPUT[3]
    population = S + E + I + R
    set_path_exp(model, 'S', 'E', 'beta*S*I')
    set_path_parameters(model, 'S', 'E', 'beta', beta/population)
    set_path_exp(model, 'E', 'I', 'epsilon*E')
    set_path_parameters(model, 'E', 'I', 'epsilon', epsilon)
    set_path_exp(model, 'I', 'R', 'gamma*I')
    set_path_parameters(model, 'I', 'R', 'gamma', gamma)
    init_value = {'S': S, 'E': E, 'I': I, 'R': R}
    init_compartment(model, init_value)
    return model


if __name__ == '__main__':
    days = 365
    S = 100000
    E = 20
    I = 10
    R = 0
    population = S + E + I + R
    INPUT = [S, E, I, R]
    beta = 0.5
    epsilon = 0.1
    gamma = 0.1
    model = get_SEIR_base_eqs(INPUT, beta, epsilon, gamma)
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
    visual_compartment_values(model)
    cases = []
    for i in range(days):
        cases.append(values['E'][i] * epsilon)
    result = {'simulate daily cases': cases}
    plot_line(result)