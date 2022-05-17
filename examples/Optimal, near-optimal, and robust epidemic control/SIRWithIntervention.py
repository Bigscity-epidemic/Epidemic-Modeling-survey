from compartment.Descriptor import vertical_divide
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment
from executor.Executor import Executor
import pandas as pd
import numpy as np
import scipy as sci

import settings as params
from examples.SIR_base_eqs.SIR_base_eqs import get_SIR_base_eqs

R0 = params.R0_default
gamma = params.gamma_default

tau = params.tau_default

inits = params.inits_default

class SIRWithIntervention():
    def __init__(self, R0 = None, gamma = None, tau = None, inits = None, strategy = ""):
        self.R0 = R0
        self.gamma = gamma
        self.inits = inits
        self.tau = tau
        self.strategy = strategy

        self.time = 0
        self.time_ts = np.array([])
        self.state_ts = np.array([[], [], []]).reshape((-1, 3))

        graph = Graph('SIR', 'S')
        vertical_divide(graph, 'S', ['I', 'R'])
        model = Model('SIR', graph)

        set_path_exp(model, 'S', 'I', 'b*beta*S*I')
        set_path_exp(model, 'I', 'R', 'gamma*I')
        set_path_parameters(model, 'S', 'I', 'beta', self.gamma * self.R0)
        set_path_parameters(model, 'S', 'I', 'b', embedding=self.getBEmbedding(strategy))
        set_path_parameters(model, 'I', 'R', 'gamma', self.gamma)


        init_value = {'S': self.inits[0], 'I': self.inits[1], 'R': self.inits[2]}
        init_compartment(model, init_value)

        self.model = model


    def getBEmbedding(self, strategy):
        pass

    def getIMax(self, allowBoundaryMax = False):
        last_timestep_error = (
            "Max at last timestep. "
            "You likely need to "
            "increase integration "
            "max time. If this was expected, "
            "set allow_boundary_max = True")
        first_timestep_error = (
            "Max at first timestep. "
            "Your model may be misspecified. "
            "If this was expected, "
            "set allow_boundary_max = True")
        ## check that we didn't get a boundary soln
        wheremax = np.argmax(self.state_ts[:, 1])
        if not allowBoundaryMax:
            if wheremax == self.state_ts[:, 1].size:
                raise ValueError(last_timestep_error)
            elif wheremax == 0:
                raise ValueError(first_timestep_error)
        return self.state_ts[wheremax, 1]

    def IOfS(self, S):
        #I0+(S0-S)+log(S/S0)/R0
        S0, I0, Rec0 = self.inits
        return (I0 + S0 - S
                - (1 / self.R0) * np.log(S0)
                - (1 / self.R0) * np.log(S))

    def tOfSTarget(self, STarget):
        '''
        How long does it take to make number of S reach STarget
        '''
        S0, I0, Rec0 = self.inits
        if np.isnan(STarget):
            raise ValueError("Cannot find time "
                             "for non-numeric/nan S\n\n"
                             "check that S is being "
                             "calculated correctly")

        def deriv(t, SVal):
            I = self.I_of_S(SVal)
            return -1 / (self.R0 * self.gamma * SVal * I)

        return sci.odeint(deriv, 0, np.linspace(S0, STarget, 2))[-1]

    def deriv(self, state, time):
        S, I, R = state
        beta = self.R0 * self.gamma
        b = self.b_func(time, beta, self.gamma, S, I)

        dS = -b * beta * S * I
        dI = b * beta * S * I - self.gamma * I
        dR = self.gamma * I


class Intervention():
    def __init__(self, tau=None, t_i=None, sigma=None, f=None, S_i_expected=None, I_i_expected=None, strategy=None):
        self.tau = tau
        self.t_i = t_i
        self.sigma = sigma
        self.f = f
        self.S_i_expected = S_i_expected
        self.I_i_expected = I_i_expected
        self.strategy = strategy

        self.repertoire = {
            "fixed": self.fixed_b,
            "maintain-suppress-time": self.maintain_suppress_time,
            "full-suppression": self.fixed_b}

    def __call__(self, time, beta, gamma, S, I):
        return self.repertoire[self.strategy](time, beta, gamma, S, I)

    def fixed_b(self, time, beta, gamma, S, I):
        if time >= self.t_i and time < self.t_i + self.tau:
            return self.sigma
        else:
            return 1

    def maintain_suppress_time(self, time, beta, gamma, S, I):
        if time >= self.t_i and time < self.t_i + self.tau * self.f:
            S_expected = (self.S_i_expected -
                          gamma * (time - self.t_i) *
                          self.I_i_expected)
            return  gamma / (beta * S_expected)

        elif (time >= self.t_i + self.tau * self.f and
              time < self.t_i + self.tau):
            return 0
        else:
            return 1



