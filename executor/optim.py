from formula import formula
from loss import loss
import scipy.integrate as spi


def optim_fun(args):
    INPUT, t_range, TRUE, kind = args
    v = lambda x: loss(TRUE, spi.odeint(formula, (INPUT[0], INPUT[1], INPUT[2], INPUT[3]), t_range, args=(x[0], x[1], x[2])))
    return v
