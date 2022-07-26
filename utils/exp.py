import math
from matplotlib import pyplot as plt
import numpy as np


def beta2mob_single(beta, betamax, betamin, mobmax, mobmin, coe):
    v = (beta - betamin) / (betamax - betamin)
    u = (math.exp(coe * v) - 1) / (math.exp(coe) - 1)
    y = u * (mobmax - mobmin) + mobmin
    return y


def beta2mob_array(beta, betamax, betamin, mobmax, mobmin, coe):
    result = []
    for item in beta:
        result.append(beta2mob_single(item, betamax, betamin, mobmax, mobmin, coe))
    return result


def mob2beta_single(mob, betamax, betamin, mobmax, mobmin, coe):
    u = (mob - mobmin) / (mobmax - mobmin)
    v = math.log(u * (math.exp(coe) - 1) + 1) / coe
    x = v * (betamax - betamin) + betamin
    return x


def mob2beta_array(mob, betamax, betamin, mobmax, mobmin, coe):
    result = []
    for item in mob:
        result.append(mob2beta_single(item, betamax, betamin, mobmax, mobmin, coe))
    return result


if __name__ == '__main__':
    beta = np.linspace(1.0, 4.0, 100)
    mobility = beta2mob_array(beta, 4.0, 1.0, 1.0, -3.0, 5.0)
    beta = mob2beta_array(mobility, 4.0, 1.0, 1.0, -3.0, 5.0)
    plt.plot(beta)
    plt.plot(mobility)
    plt.show()
