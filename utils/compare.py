import math

import numpy as np

def get_MAE(TRUE, PRED):
    length = TRUE.shape[0]
    res = 0
    for i in range(length):
        y_=TRUE[i]
        y = PRED[i]
        res += abs(y-y_)
    return res/length

def get_MSE(TRUE, PRED):
    length = TRUE.shape[0]
    res = 0
    for i in range(length):
        y_ = TRUE[i]
        y = PRED[i]
        res += (y - y_)**2
    return res / length

def get_RMSE(TRUE, PRED):
    length = TRUE.shape[0]
    res = 0
    for i in range(length):
        y_ = TRUE[i]
        y = PRED[i]
        res += (y - y_) ** 2
    return math.sqrt(res/length)

def get_MAPE(TRUE, PRED):
    length = TRUE.shape[0]
    res = 0
    for i in range(length):
        y_ = TRUE[i]
        y = PRED[i]
        res += abs((y - y_)/y)
    return res / length

def get_R2(TRUE, PRED):
    length = TRUE.shape[0]
    res1 = 0
    res2 = 0
    sum = 0
    for i in PRED:
        sum += i
    mean = sum / length
    for i in range(length):
        y_ = TRUE[i]
        y = PRED[i]
        res1 += (y - y_) ** 2
        res2 += (y-mean) **2
    return 1 - res1/res2
