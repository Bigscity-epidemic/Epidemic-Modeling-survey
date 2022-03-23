from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide, horizontal_divide
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line


def get_SUEIR(INPUT, beta, sigma, pho, epsilon, _lambda_, gamma):
    graph = Graph('SUEIR', 'S')
    vertical_divide(graph, 'S', ['E', 'I', 'R'])
    horizontal_divide(graph, 'I', ['IS'])
    model = Model('SUEIR', graph)
    S = INPUT[0]
    E = INPUT[1]
    I = INPUT[2]
    IS = INPUT[3]
    R = INPUT[4]
    beta = max(beta, 0)
    sigma = max(sigma, 0)
    pho = max(pho, 0)
    epsilon = max(epsilon, 0)
    _lambda_ = max(_lambda_, 0)
    _lambda_ = min(_lambda_, 1)
    gamma = max(gamma, 0)
    set_path_exp(model, 'S', 'E', 'beta*S*I+sigma*S*param_max')
    set_path_parameters(model, 'S', 'E', 'beta', beta)
    set_path_parameters(model, 'S', 'E', 'sigma', sigma)
    set_path_parameters(model, 'S', 'E', 'param_max', 0)
    set_path_exp(model, 'E', 'I', 'param_lambda*epsilon*E')
    set_path_parameters(model, 'E', 'I', 'param_lambda', (1-_lambda_))
    set_path_parameters(model, 'E', 'I', 'epsilon', epsilon)
    set_path_exp(model, 'E', 'IS', 'lambda*epsilon*E')
    set_path_parameters(model, 'E', 'IS', 'lambda', _lambda_)
    set_path_parameters(model, 'E', 'IS', 'epsilon', epsilon)
    set_path_exp(model, 'I', 'R', 'gamma*I')
    set_path_parameters(model, 'I', 'R', 'gamma', gamma)
    set_path_exp(model, 'IS', 'R', 'gamma*IS')
    set_path_parameters(model, 'IS', 'R', 'gamma', gamma)
    init_value = {'S': S, 'E': E, 'I': I, 'IS': IS, 'R': R}
    init_compartment(model, init_value)
    return model


if __name__ == '__main__':
    foo_length = 24
    fit_length = 6
    history_length = foo_length + fit_length
    future_length = 120
    df_data = {'confirm': [], 'death': [], 'recover': []}
    df_file = open('hongkong-data.csv', encoding='utf8')
    for kind in ['confirm', 'death', 'recover']:
        line = df_file.readline().split(',')
        for item in line[-history_length:]:
            figure = item.replace('\n', '')
            df_data[kind].append(float(figure))
    data = []
    for i in range(1, history_length):
        data.append(df_data['confirm'][i] - df_data['confirm'][i - 1])
    # part1
    S = 7482000
    E = 30816.0
    I = 1823.2
    IS = 455.8
    R = 13129.0
    INPUT = [S, E, I, IS, R]
    beta = 0.0
    sigma = 0.00000003
    pho = 0.0
    epsilon = 0.01000759
    _lambda_ = 12.0200998
    gamma = 0.0
    model1 = get_SUEIR(INPUT, beta, sigma, pho, epsilon, _lambda_, gamma)
    visual_model(model1)
    executor1 = Executor(model1)
    values1 = model1.get_values()
    for name in values1.keys():
        values1[name] = [values1[name]]
    for index in range(foo_length):
        pre_value = model1.get_values()
        if (pre_value['E'] - (pho * pre_value['IS'])) > 0.005 * pre_value['E']:
            # print(beta*pre_value['S']*pre_value['I'] + pre_value['S'] * sigma * (pre_value['E'] - (pho * pre_value['IS'])))
            model1.reset_parameters('param_max', pre_value['E'] - (pho * pre_value['IS']))
        else:
            # print(beta * pre_value['S'] * pre_value['I'] + pre_value['S'] * sigma * (0.005*E))
            model1.reset_parameters('param_max', 0.005 * pre_value['E'])
        executor1.simulate_step(index)
        cur_value = model1.get_values()
        print(cur_value)
        for name in values1.keys():
            values1[name].append(cur_value[name])
    visual_compartment_values(model1)
    cases = []
    for i in range(1, foo_length):
        cases.append(
            values1['I'][i] + values1['IS'][i] + values1['R'][i] - values1['I'][i - 1] - values1['IS'][i - 1] - values1['R'][
                i - 1])
    # part2
    S = 7482000
    E = 587460.0
    I = 223464.0
    IS = 55866.0
    R = 14400.0
    INPUT = [S, E, I, IS, R]
    beta = 0.0
    sigma = 0.0
    pho = 14.79288606
    epsilon = 0.08980608
    _lambda_ = 5.22707102
    gamma = 0.0
    model2 = get_SUEIR(INPUT, beta, sigma, pho, epsilon, _lambda_, gamma)
    executor2 = Executor(model2)
    values2 = model2.get_values()
    for name in values2.keys():
        values2[name] = [values2[name]]
    for index in range(fit_length + future_length):
        pre_value = model2.get_values()
        if (pre_value['E'] - (pho * pre_value['IS'])) > 0.005 * pre_value['E']:
            # print(beta*pre_value['S']*pre_value['I'] + pre_value['S'] * sigma * (pre_value['E'] - (pho * pre_value['IS'])))
            model2.reset_parameters('param_max', pre_value['E'] - (pho * pre_value['IS']))
        else:
            # print(beta * pre_value['S'] * pre_value['I'] + pre_value['S'] * sigma * (0.005*E))
            model2.reset_parameters('param_max', 0.005 * pre_value['E'])
        executor2.simulate_step(index)
        cur_value = model2.get_values()
        print(cur_value)
        for name in values2.keys():
            values2[name].append(cur_value[name])
    visual_compartment_values(model2)
    for i in range(1, fit_length + future_length):
        cases.append(
            values2['I'][i] + values2['IS'][i] + values2['R'][i] - values2['I'][i - 1] - values2['IS'][i - 1] - values2['R'][
                i - 1])
    result = {'simulate daily cases': cases, 'daily cases': data}
    plot_line(result)