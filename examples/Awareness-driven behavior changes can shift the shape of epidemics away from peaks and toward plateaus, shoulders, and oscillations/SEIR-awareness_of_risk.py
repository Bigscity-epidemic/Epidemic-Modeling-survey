from compartment.Descriptor import vertical_divide, horizontal_divide
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment, reset_parameters
from executor.Executor import Executor
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line

graph = Graph('SEIR-awareness_of_risk', 'S')
print(vertical_divide(graph, 'S', ['E', 'I', 'R']))
print(horizontal_divide(graph, 'R', ['D']))
model = Model('SEIR-awareness_of_risk', graph)
visual_model(model)

# figseir_baseplat.m
beta = 0.5
mu = 0.5
gamma = 1/6
frac_D = 0.01
R0 = beta / gamma
Dcrit = 10**(-5)
awareness = 2.0
N = 10**7

days = 400
population = N
init_exposed = 1.0
init_infectious = 0.0
init_removed = 0.0
init_death = 0.0
init_susceptible = population - init_exposed - init_infectious - init_death

Dday0 = gamma*init_infectious*frac_D
Iday0 = beta*init_susceptible*init_infectious/(1+Dday0/Dcrit)**awareness

print(set_path_exp(model, 'S', 'E', 'beta*S*I'))
print(set_path_parameters(model, 'S', 'E', 'beta', beta / (1 + (Dday0 / Dcrit) ** awareness) / N))
print(set_path_exp(model, 'E', 'I', 'mu*E'))
print(set_path_parameters(model, 'E', 'I', 'mu', mu))
print(set_path_exp(model, 'I', 'R', 'gammaR*I'))
print(set_path_parameters(model, 'I', 'R', 'gammaR', gamma * (1 - frac_D)))
print(set_path_exp(model, 'I', 'D', 'gammaD*I'))
print(set_path_parameters(model, 'I', 'D', 'gammaD', gamma * frac_D))

init_value = {
    'S': init_susceptible / N,
    'E': init_exposed / N,
    'I': init_infectious / N,
    'R': init_removed / N,
    'D': init_death / N
}
print(init_compartment(model, init_value))
visual_compartment_values(model)
executor = Executor(model)
values = model.get_values()
Ddays = []
Dq = []
Idays = []
Iq = []
for name in values.keys():
    values[name] = [values[name]]
for index in range(days):
    tmp_value = model.get_values()
    Dday = gamma * tmp_value['I'] * frac_D
    Iday = beta * tmp_value['S'] * tmp_value['I'] / (1 + (Dday / Dcrit) ** awareness)
    Ddays.append(Dday*N)
    Dq.append(N*Dcrit*(R0**(1/awareness)-1)*2)
    Idays.append(Iday*N)
    Iq.append(N*Dcrit*(R0**(1/awareness)-1)*2/frac_D)
    print(reset_parameters(model, 'beta', beta / (1 + (Dday / Dcrit) ** awareness)))
    executor.simulate_step(index)
    for name in values.keys():
        values[name].append(tmp_value[name]*N)
visual_compartment_values(model)
resultI = {'Infectious / day': Idays, 'Infection rate plateau': Iq}
plot_line(resultI, log=False)
resultD = {'Deaths / day': Ddays, 'Fatality rate plateau': Dq}
plot_line(resultD, log=False)