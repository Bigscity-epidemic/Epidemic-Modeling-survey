from compartment.Descriptor import vertical_divide, add_path
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment
from executor.Executor import Executor
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line


def get_SIR_eqs(INPUT, Lambda, beta, gamma, mu):
    graph = Graph('SIR_eqs', 'S0')
    vertical_divide(graph, 'S0', ['S', 'I', 'R'])
    graph.add_single_node('D0')
    add_path(graph, 'S', 'D0')
    add_path(graph, 'I', 'D0')
    add_path(graph, 'R', 'D0')
    model = Model('SIR_eqs', graph)
    S0 = 2147483647
    S = INPUT[0]
    I = INPUT[1]
    R = INPUT[2]
    D0 = 0
    population = S + I + R
    set_path_exp(model, 'S0', 'S', 'lambda')
    set_path_parameters(model, 'S0', 'S', 'lambda', Lambda)
    set_path_exp(model, 'S', 'I', 'beta*S*I')
    set_path_parameters(model, 'S', 'I', 'beta', beta/population)
    set_path_exp(model, 'I', 'R', 'gamma*I')
    set_path_parameters(model, 'I', 'R', 'gamma', gamma)
    set_path_exp(model, 'S', 'D0', 'mu_S*S')
    set_path_parameters(model, 'S', 'D0', 'mu_S', mu)
    set_path_exp(model, 'I', 'D0', 'mu_I*I')
    set_path_parameters(model, 'I', 'D0', 'mu_I', mu)
    set_path_exp(model, 'R', 'D0', 'mu_R*I')
    set_path_parameters(model, 'R', 'D0', 'mu_R', mu)
    init_value = {'S0': S0, 'S': S, 'I': I, 'R': R, 'D0': D0}
    init_compartment(model, init_value)
    return model

if __name__ == '__main__':
    days = 365
    S = 10000
    I = 10
    R = 0
    population = S + I + R
    INPUT = [S, I, R]
    Lambda = 100
    beta = 0.5
    gamma = 0.1
    mu = 0.01
    model = get_SIR_eqs(INPUT, Lambda, beta, gamma, mu)
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
        cases.append(values['I'][i] * values['S'][i] * beta / population)
    result = {'simulate daily cases': cases}
    plot_line(result)