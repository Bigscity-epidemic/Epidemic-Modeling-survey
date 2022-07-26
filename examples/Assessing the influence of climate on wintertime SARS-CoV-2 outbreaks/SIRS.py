from compartment.Descriptor import vertical_divide
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment
from executor.Executor import Executor
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line
import pandas as pd
import numpy as np

'''
SIRS model
L means after L days a Recovered person can transfer to a Susceptible Person again
D is the mean infectious period
'''

# according to the paper
days = 2000

beta = []
gamma = 0

L = 66.25*7
D = 5
population = 8000000

R0min = 1.5
R0max = 2.5
Immunity = 66.25*7
Var = -227.5
SHAT = pd.read_csv("Data/NYq.csv")['x']
pop = population




def runModel(Lead, R0list, SSet = 'Orig', ISet = 'Orig', Rchange = 1):
    qout = SHAT
    if(Lead == 0):
        qout = np.repeat(qout, 7)
    else:
        qout = np.repeat(qout, 7)
        qout = np.concatenate((qout[Lead-1:], qout[:Lead-1]), axis = 0)
    qout = np.tile(qout, int(days/len(qout))+1)
    R0 = np.exp(Var*qout + np.log(R0max - R0min)) + R0min
    R0 = R0 * Rchange

    for i in range(len(R0list)):
        R0[i] = R0list[i]

    beta = [R / (D * pop) for R in R0]
    x= 0
    for b in beta:
        x+=1
        if b > 1e-5:
            print(x)
            exit(0)
    if(SSet == 'Orig'):
        S0 = pop -1
    else:
        S0 = pop * SSet
    if type(ISet) == str and ISet == 'Orig':
        I0 = 1
    else:
        I0 = ISet
        S0 = S0 - I0

    R0_ = pop - S0 - I0


    input = [S0, I0, R0_]
    model = get_SIRS(input, beta)

    executor = Executor(model)

    values = model.get_values()
    for name in values.keys():
        values[name] = [values[name]]
    for index in range(days):
        executor.simulate_step(index)
        tmp_value = model.get_values()
        for name in values.keys():
            values[name].append(tmp_value[name])
    values['R0'] = R0
    return values

def get_SIRS(INPUT, beta):
    graph = Graph('SIRS', 'S')
    vertical_divide(graph, 'S', ['I', 'R'])
    graph.add_next('R','S')
    model = Model('SIRS', graph)
    S = INPUT[0]
    I = INPUT[1]
    R = INPUT[2]

    set_path_exp(model, 'S', 'I', 'beta*S*I')
    set_path_parameters(model, 'S', 'I', 'beta', embedding=beta)
    set_path_exp(model, 'I', 'R', 'gamma*I')
    set_path_parameters(model, 'I', 'R', 'gamma', 1/D)
    set_path_exp(model, 'R', 'S', 'R*theta')
    set_path_parameters(model, 'R', 'S', 'theta', 1/L)
    init_value = {'S': S, 'I': I, 'R': R}
    init_compartment(model, init_value)
    return model


