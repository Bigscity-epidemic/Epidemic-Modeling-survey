from math import log


def get_logindex(array):
    result = []
    for i in range(len(array) - 1):
        result.append(log(array[i + 1]) - log((array[i])))
    return result
