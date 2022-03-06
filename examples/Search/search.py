import numpy as np

from examples.SEIR_base_eqs.SEIR_base_eqs import get_SEIR_base_eqs
from examples.SEIR_eqs.SEIR_eqs import get_SEIR_eqs
from examples.SIR_base_eqs.SIR_base_eqs import get_SIR_base_eqs
from examples.SIR_eqs.SIR_eqs import get_SIR_eqs
from executor.Executor import Executor
from visual.visual_graph import visual_model


def loss_func(TRUE, PRED):
    return np.sum(np.square((TRUE[:, 0] - TRUE[:, 1]) - PRED[:, 2])) + np.sum(np.square(TRUE[:, 1] - PRED[:, 3]))


def simulate(model, days):
    executor = Executor(model)
    visual_model(model)
    values = model.get_values()
    for name in values.keys():
        values[name] = [values[name]]
    for index in range(days):
        executor.simulate_step(index)
        tmp_value = model.get_values()
        for name in values.keys():
            values[name].append(tmp_value[name])
    if 'E' in values:
        return np.array([values['S'], values['E'], values['I'], values['R']]).T
    else:
        return np.array([values['S'], values['S'], values['I'], values['R']]).T

# TRUE = [total_infect_data[], total_remove_data[]].T
# INPUT = [S, E, I, R]
# PARAMS = [Lambda, beta, epsilon, gamma, mu]
def search(TRUE, INPUT, PARAMS):
    days = np.shape(TRUE)[0]-1
    print(days)
    INPUT_SEIR = INPUT if len(INPUT) == 4 else [INPUT[0], 2*INPUT[1], INPUT[1], INPUT[2]]
    INPUT_SIR = INPUT if len(INPUT) == 3 else [INPUT[0] + INPUT[1], INPUT[2], INPUT[3]]
    Lambda = PARAMS[0]
    beta = PARAMS[1]
    epsilon = PARAMS[2]
    gamma = PARAMS[3]
    mu = PARAMS[4]
    PREDS = []
    model_SIR_base = get_SIR_base_eqs(INPUT_SIR, beta, gamma)
    PREDS.append(simulate(model_SIR_base, days))
    model_SIR = get_SIR_eqs(INPUT_SIR, Lambda, beta, gamma, mu)
    PREDS.append(simulate(model_SIR, days))
    model_SEIR_base = get_SEIR_base_eqs(INPUT_SEIR, beta, epsilon, gamma)
    PREDS.append(simulate(model_SEIR_base, days))
    model_SEIR = get_SEIR_eqs(INPUT_SEIR, Lambda, beta, epsilon, gamma, mu)
    PREDS.append(simulate(model_SEIR, days))
    loss = -1
    res = []
    for PRED in PREDS:
        if loss == -1:
            loss = loss_func(TRUE, PRED)
            res = PRED
        else:
            if loss_func(TRUE, PRED) < loss:
                loss = loss_func(TRUE, PRED)
                res = PRED
    return res
'''
    [1e-6, 9e-7, 10, 0.3, 0.95, 9e-2]
    x[0] = E[0]
    x[1] = beta
    x[2] = sigma
    x[3] = epsilon
    x[4] = _lambda_
    x[5] = gamma
    '''

if __name__ == '__main__':
    TRUE = np.array([[412617575.0, 337354007.0],
 [414386435.0, 340206105.0],
 [416773487.0, 342945691.0],
 [418805148.0, 345698483.0],
 [420753948.0, 348098915.0],
 [422298116.0, 350143481.0],
 [423558952.0, 352255394.0],
 [425077781.0, 354800619.0]])
    INPUT = [500000000, 66018812.0, 75263568.0, 337354007.0]
    population = INPUT[0] + INPUT[1] + INPUT[2] + INPUT[3]
    PRAMAS = [1000, 9e-7, 0.3, 9e-2, 1000/population]
    print(search(TRUE, INPUT, PRAMAS))

