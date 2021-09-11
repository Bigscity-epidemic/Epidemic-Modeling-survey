import numpy as np


def formula(INPUT, t, beta, alpha, gamma):
    Y = np.zeros(4)
    S = INPUT[0]
    E = INPUT[1]
    I = INPUT[2]
    R = INPUT[3]
    Y[0] = - (beta*S*I)   # dS/dt
    Y[0] = + (beta*S*I) - (alpha*E)   # dE/dt
    Y[0] = + (alpha*E) - (gamma*I)   # dI/dt
    Y[0] = + (gamma*I)   # dR/dt
    return Y
