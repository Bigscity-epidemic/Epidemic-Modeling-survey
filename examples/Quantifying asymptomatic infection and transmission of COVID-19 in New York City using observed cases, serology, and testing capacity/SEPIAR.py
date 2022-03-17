import csv
from math import exp
from compartment.Descriptor import vertical_divide, horizontal_divide
from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment
from executor.Executor import Executor
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values
from visual.visual_value_line import plot_line

graph = Graph('SEPIAR', 'S')
print(vertical_divide(graph, 'S', ['E', 'I_P', 'I_S_1']))
print(vertical_divide(graph, 'E', ['E1', 'E2', 'E3', 'E4']))
print(horizontal_divide(graph, 'I_S_1', ['I_A']))
print(vertical_divide(graph, 'I_S_1', ['I_S_2']))
print(vertical_divide(graph, 'I_A', ['R_A']))
print(horizontal_divide(graph, 'I_S_2', ['I_H']))
print(vertical_divide(graph, 'I_S_2', ['R_F']))
print(vertical_divide(graph, 'I_H', ['R_H']))
model = Model('SEPIAR', graph)
visual_model(model)

# 默认参数，见 NYC_COVID_DATA_SEIAR_and_SEPIAR.Rmd
phi_E = 1.09 # 迷惑参数
phi_U = phi_E
phi_S = 1/5
h_V = 1/13 # 住院恢复率（13天出院）
p_S = 0.15 # 症状比例
p_H_cond_S = 0.30 # 住院比例（重症）
gamma = 1/3 # 轻症恢复天数
PCR_sens = 0.90 #
b_a = 1 # 无症状传染率与有症状传染率之比
R_0 = 10.25 # 有症状的日传染数
b_q = 0.08 # 干预后传染率与有症状传染率之比
b_p = 0.0 # 症状前传染率与有症状传染率之比
E_0 = 15200 # 初始暴露人数
z_0 = 15200 # 初始感染人数
N_0 = 8.0e6 # 总人数
C_0 = 0.0
sigma_M = 0.25 # 没用
G_w_y_scaling = 0.162 # 没用

# Appendix figure 11 A 参数
# low b_a
b_a = 0.07
R_0 = 6.10
b_q = 0.23
b_p = 0.94
p_S = 0.15
p_H_cond_S = 0.16
gamma = 6.33
E_0 = 63566.34
z_0 = 13443.0

# Appendix figure 11 B 参数
# high b_a
b_a = 0.97
R_0 = 3.08
b_q = 0.16
b_p = 0.99
p_S = 0.15
p_H_cond_S = 0.17
gamma = 11.73
E_0 = 54806.0
z_0 = 11625.0

population = N_0
init_exposed = E_0
init_infectious = z_0
init_removed = 0.0
init_susceptible = population - init_exposed - init_infectious

# 初始化各仓室人数，见 Csnippet_nyc_coronavirus_model_N_12.R
I_init_total = z_0
time_pre_symp = 1 / phi_U
time_symp = 1 / phi_S
prop_time_pre_symp = time_pre_symp / (time_pre_symp + time_symp)
total_init_I_symp = p_S * I_init_total
I_A = (1-p_S) * I_init_total
I_P = prop_time_pre_symp * total_init_I_symp
I_S_1 = (1-prop_time_pre_symp) * total_init_I_symp
I_S_2 = 0.0
I_H = 0.0
R_A = 0.0
R_F = 0.0
R_H = 0.0

days = 89 # 仿真时间
total_time_infected = (1/gamma) + (1/phi_S)
gamma_total = 1/total_time_infected
Beta_0 = R_0*gamma_total / N_0
Beta_1 = b_q*Beta_0 / N_0
beta_t = []
quarantine_start_time = 22 # 03-01 ~ 03-23
social_distancing_start_time = 18 # 03-01 ~ 03-19
for i in range(days):
    beta_t.append(Beta_0)
for i in range(quarantine_start_time, days):
    beta_t[i] = Beta_1
for i in range(social_distancing_start_time, quarantine_start_time):
    m_q = (Beta_1 - Beta_0) / (quarantine_start_time - social_distancing_start_time)
    beta_t[i] = Beta_0 + m_q * (i - social_distancing_start_time)
beta_p = [] # transmission rates in pre-symptomatic classes
for i in range(days):
    beta_p.append(b_p * beta_t[i])
beta_a = [] # transmission rates in asymptomatic classes
for i in range(days):
    beta_a.append(b_a * beta_t[i])

# 转移方程，见 Csnippet_nyc_coronavirus_model_N_12.R
# phi_E, phi_U, phi_S 的含义有点迷惑，似乎代表时间
print(set_path_exp(model, 'S', 'E', 'beta_t*S*I_S_1+beta_t*S*I_S_2+beta_a*S*I_A+beta_p*S*I_P'))
print(set_path_parameters(model, 'S', 'E', 'beta_t', embedding=beta_t))
print(set_path_parameters(model, 'S', 'E', 'beta_a', embedding=beta_a))
print(set_path_parameters(model, 'S', 'E', 'beta_p', embedding=beta_p))
print(set_path_exp(model, 'E', 'E1', 'phi_E_0_1*E'))
print(set_path_parameters(model, 'E', 'E1', 'phi_E_0_1', 1 - exp(-phi_E)))
print(set_path_exp(model, 'E1', 'E2', 'phi_E_1_2*E1'))
print(set_path_parameters(model, 'E1', 'E2', 'phi_E_1_2', 1 - exp(-phi_E)))
print(set_path_exp(model, 'E2', 'E3', 'phi_E_2_3*E2'))
print(set_path_parameters(model, 'E2', 'E3', 'phi_E_2_3', 1 - exp(-phi_E)))
print(set_path_exp(model, 'E3', 'E4', 'phi_E_3_4*E3'))
print(set_path_parameters(model, 'E3', 'E4', 'phi_E_3_4', 1 - exp(-phi_E)))
print(set_path_exp(model, 'E4', 'I_P', 'phi_E*E4'))
print(set_path_parameters(model, 'E4', 'I_P', 'phi_E', 1 - exp(-phi_E)))
print(set_path_exp(model, 'I_P', 'I_S_1', 'mu_I_P_I_S_1*I_P'))
print(set_path_parameters(model, 'I_P', 'I_S_1', 'mu_I_P_I_S_1', p_S*phi_U))
print(set_path_exp(model, 'I_P', 'I_A', 'mu_I_P_I_A*I_P'))
print(set_path_parameters(model, 'I_P', 'I_A', 'mu_I_P_I_A', (1-p_S)*phi_U))
print(set_path_exp(model, 'I_S_1', 'I_S_2', 'mu_I_S_1_I_S_2*I_S_1'))
print(set_path_parameters(model, 'I_S_1', 'I_S_2', 'mu_I_S_1_I_S_2', (1-p_H_cond_S)*phi_S))
print(set_path_exp(model, 'I_S_1', 'I_H', 'mu_I_S_1_I_H*I_S_1'))
print(set_path_parameters(model, 'I_S_1', 'I_H', 'mu_I_S_1_I_H', p_H_cond_S*phi_S))
print(set_path_exp(model, 'I_A', 'R_A', 'phi_S*I_A'))
print(set_path_parameters(model, 'I_A', 'R_A', 'phi_S', 1 - exp(-phi_S)))
print(set_path_exp(model, 'I_S_2', 'R_F', 'gamma*I_S_2'))
print(set_path_parameters(model, 'I_S_2', 'R_F', 'gamma', 1 - exp(-gamma)))
print(set_path_exp(model, 'I_H', 'R_H', 'h_v*I_H'))
print(set_path_parameters(model, 'I_H', 'R_H', 'h_v', 1 - exp(-h_V)))
init_value = {'S': init_susceptible,
              'E': init_exposed / 5, 'E1': init_exposed / 5, 'E2': init_exposed / 5, 'E3': init_exposed / 5, 'E4': init_exposed / 5,
              'I_P': I_P,
              'I_A': I_A,
              'I_S_1': I_S_1,
              'I_S_2': I_S_2,
              'I_H': I_H,
              'R_F': R_F,
              'R_H': R_H,
              'R_A': R_A
              }
print(init_compartment(model, init_value))
visual_compartment_values(model)
executor = Executor(model)
values = model.get_values()
for name in values.keys():
    values[name] = [values[name]]
for index in range(days):
    executor.simulate_step(index)
    tmp_value = model.get_values()
    for name in values.keys():
        values[name].append(tmp_value[name])
visual_compartment_values(model)
cases = []
for i in range(days):
    cases.append(values['I_S_1'][i]*(1-p_H_cond_S)*phi_S + values['I_S_1'][i]*p_H_cond_S*phi_S) # 日新增病例数
result = {'simulate daily cases': cases}
print(result)

with open(r".\observed_data_N_12.csv") as c:
    r = csv.reader(c)
    data = []
    index = 0
    for i in r:
        if index != 0:
            data.append(float(i[0]))
        index += 1
result.update({'observed daily cases': data})
plot_line(result, log=False)