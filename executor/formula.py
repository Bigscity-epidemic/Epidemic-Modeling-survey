import numpy as np


def formula(INPUT, t, beta, alpha, gamma):
    Y = np.zeros(4)
    S = INPUT[0]
    E = INPUT[1]
    I = INPUT[2]
    R = INPUT[3]
