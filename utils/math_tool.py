import numpy as np

def get_sum(array):
    return np.sum(array)

def get_mean(array):
    return np.average(array)

def get_var(array):
    return np.var(array)

def get_std(array):
    return np.std(array)

def get_diff(array):
    return np.diff(array)

def get_log_diff(array):
    logArray = np.log10(array)
    return np.diff(logArray)

def get_normalization(array):
    updown = np.max(array) - np.min(array)
    return (array - np.min(array)) / updown

def get_standardization(array):
    mu = np.mean(array, axis = 0)
    sigma = np.std(array, axis = 0)
    return (array - mu) / sigma