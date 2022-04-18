from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide, horizontal_divide, add_path
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters, reset_parameters
from visual.visual_value_line import plot_line
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values

graph = Graph('SCIR', 'S')
print(vertical_divide(graph, 'S', ['C']))
print(horizontal_divide(graph, 'C', ['I']))
print(vertical_divide(graph, 'I', ['R']))
print(horizontal_divide(graph, 'R', ['D']))
print(add_path(graph, 'C', 'S'))
model = Model('SCIR', graph)


N = 1000000  # 初始人数
S_0 = N  # 初始S舱室人数
C_0 = 0
I_0 = 1
R_0 = 0
D_0 = 0

days = 80

q = 0.062  # 封城系数
p = 0.007  # 解除封城系数
beta = 0.425  # 感染系数
mu = 0  # 致死系数
r = 0.021  # 治愈系数

q = [0] * 13 + [0.062] * 67

set_path_exp(model, 'S', 'C', 'q*S')
set_path_parameters(model, 'S', 'C', 'q', embedding=q)
set_path_exp(model, 'C', 'S', 'p*C')
set_path_parameters(model, 'C', 'S', 'p', p)
set_path_exp(model, 'S', 'I', 'beta*S*I')
set_path_parameters(model, 'S', 'I', 'beta', beta / N)
set_path_exp(model, 'I', 'D', 'mu*I')
set_path_parameters(model, 'I', 'D', 'mu', mu)
set_path_exp(model, 'I', 'R', 'r*I')
set_path_parameters(model, 'I', 'R', 'r', r)
visual_model(model)
init_value = {
    'S': S_0,
    'C': C_0,
    'I': I_0,
    'R': R_0,
    'D': D_0
}

init_compartment(model, init_value)

executor = Executor(model)
values = model.get_values()

for name in values.keys():
    values[name] = [values[name]]

for index in range(days):
    executor.simulate_step(index)
    tmp_values = model.get_values()
    for name in values.keys():
        values[name].append(tmp_values[name])

visual_compartment_values(model)
result = {'Active Cases': values['I']}
plot_line(result, log=True)
