import math


def exp_dynamic(parameter_max, parameter_min, vector, coe):
    updown = math.log(parameter_max - parameter_min)
    result = []
    for item in vector:
        tmp = coe * item + updown
        result.append(math.exp(tmp) + parameter_min)

    return result
