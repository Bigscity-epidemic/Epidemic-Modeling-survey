import numpy as np


def get_daily(TRUE, PRED):
    tmpTrue = TRUE.copy()
    tmpPred = np.array(PRED).copy()
    for i in range(1, len(TRUE), 1):
        k = len(TRUE) - i
        for j in range(len(tmpTrue[k])):
            tmpTrue[k][j] -= tmpTrue[k - 1][j]
        for j in range(len(tmpPred[k])):
            tmpPred[k][j] -= tmpPred[k - 1][j]
    for j in range(len(tmpTrue[0])):
        tmpTrue[0][j] = 0.0
    for j in range(len(tmpPred[0])):
        tmpPred[0][j] = 0.0
    return tmpTrue, tmpPred 


def loss(TRUE, PRED):
    tt, tp = get_daily(TRUE, PRED)
    return np.sum(np.square((tt[:, 0]) - (tp[:, 2] + tp[:, 3])) + np.square((tt[:, 1]) - (tp[:, 3])))
