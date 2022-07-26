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
    days = 20
    S = 100
    I = 10
    R = 0
    population = S + I + R
    INPUT = [S, I, R]
    beta = 0.7
    gamma = 0.4
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
    cases = []
    for i in range(days):
        cases.append(values['I'][i] * values['S'][i] * beta / population)
    for i in range(20):
        cases.append(cases[-1] * 0.8)
    cases1 = [0] * 4 + cases[:-4]
    cases2 = [0] * 6 + cases1[:-6]
    cases3 = [0] * 1 + cases2[:-1]
    cases4 = [0] * 3 + cases3[:-3]

    sumcase = []
    for i in range(40):
        sumcase.append(cases[i] + cases1[i] + cases2[i] + cases3[i] + cases4[i])
    fake=[0]*25
    fake[24]=1000
    plt.figure(figsize=(7, 5))
    plt.plot(cases[:25], 'o-', label='第一传播链日新增确诊病例数')
    plt.plot(cases1[:25], 'o-', label='第二传播链日新增确诊病例数')
    plt.plot(cases2[:25], 'o-', label='第三传播链日新增确诊病例数')
    plt.plot(cases3[:25], 'o-', label='第四传播链日新增确诊病例数')
    plt.plot(cases4[:25], 'o-', label='第五传播链日新增确诊病例数')
    plt.plot(fake[:25], 'o-', label='该地区报告日新增确诊病例数')
    #plt.grid("True")
    plt.legend(loc='upper left', prop=myfont, frameon=False)
    # plt.title(u'北、上、深疫情情况对比'.format('某地区', '某时间'), FontProperties=myfont)
    plt.xlabel('天数', size=14)
    plt.ylabel('病例数', size=14)
    plt.savefig('1.jpg', dpi=300, bbox_inches='tight')
    plt.show()
