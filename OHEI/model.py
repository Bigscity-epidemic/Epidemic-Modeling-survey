from executor.Executor import Executor
from graph import get_eqs
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment


def get_model(age_enum, init_comp, _lambda, _v, _omega_n, _omega_v, _e, _p_a, _sigma, _gamma_i, _gamma_p, _gamma_s,
              _gamma_c):
    # calculate population
    population = {}
    for age in age_enum:
        population[age] = 0.0
        for comp_name in init_comp[age].keys():
            population[age] += init_comp[age][comp_name]

    # create models
    age2models = {}
    for age in age_enum:
        model = get_eqs()
        set_path_exp(model, 'S', 'V', 'v')
        set_path_parameters(model, 'S', 'V', 'v', _v[age])

        set_path_exp(model, 'S', 'E', 'S*lambda')
        set_path_parameters(model, 'S', 'E', 'lambda', _lambda[age])

        set_path_exp(model, 'V', 'S', 'V*omegav')
        set_path_parameters(model, 'V', 'S', 'omegav', _omega_v[age])

        set_path_exp(model, 'V', 'E', 'V*lambda*e_anti*pa_anti')
        set_path_parameters(model, 'V', 'E', 'lambda', _lambda[age])
        set_path_parameters(model, 'V', 'E', 'e_anti', 1.0 - _e[age])
        set_path_parameters(model, 'V', 'E', 'pa_anti', 1.0 - _p_a[age])

        set_path_exp(model, 'V', 'Ev', 'V*lambda*e_anti*pa+outcome')
        set_path_parameters(model, 'V', 'Ev', 'lambda', _lambda[age])
        set_path_parameters(model, 'V', 'Ev', 'e_anti', 1.0 - _e[age])
        set_path_parameters(model, 'V', 'Ev', 'pa', _p_a[age])
        set_path_parameters(model, 'V', 'Ev', 'outcome', 5.0)

        set_path_exp(model, 'E', 'Ip', 'E*sigma*gammai')
        set_path_parameters(model, 'E', 'Ip', 'sigma', _sigma[age])
        set_path_parameters(model, 'E', 'Ip', 'gammai', _gamma_i[age])

        set_path_exp(model, 'E', 'Is', 'E*sigma*gammai_anti')
        set_path_parameters(model, 'E', 'Is', 'sigma', _sigma[age])
        set_path_parameters(model, 'E', 'Is', 'gammai_anti', 1.0 - _gamma_i[age])

        set_path_exp(model, 'Ev', 'Is', 'Ev*sigma')
        set_path_parameters(model, 'Ev', 'Is', 'sigma', _sigma[age])

        set_path_exp(model, 'Ip', 'Ic', 'Ip*gammap')
        set_path_parameters(model, 'Ip', 'Ic', 'gammap', _gamma_p[age])

        set_path_exp(model, 'Is', 'R', 'Is*gammas')
        set_path_parameters(model, 'Is', 'R', 'gammas', _gamma_s[age])

        set_path_exp(model, 'Ic', 'R', 'Ic*gammac')
        set_path_parameters(model, 'Ic', 'R', 'gammac', _gamma_c[age])

        set_path_exp(model, 'R', 'S', 'R*omegan')
        set_path_parameters(model, 'R', 'S', 'omegan', _omega_n[age])

        init_compartment(model, init_comp[age])
        age2models[age] = model

    return age2models


if __name__ == '__main__':
    ages = ['0', '1']
    ic = {'0': {'S': 10000.0, 'E': 2.0, 'Ip': 1.0, 'Ic': 1.0, 'R': 100.0, 'V': 20000.0, 'Ev': 3.0, 'Is': 0.0},
          '1': {'S': 50000.0, 'E': 2.0, 'Ip': 1.0, 'Ic': 1.0, 'R': 100.0, 'V': 30000.0, 'Ev': 3.0, 'Is': 0.0}}
    l = {'0': 0.001, '1': 0.002}
    v = {'0': 0.003, '1': 0.004}
    on = {'0': 0.005, '1': 0.006}
    ov = {'0': 0.007, '1': 0.008}
    e = {'0': 0.009, '1': 0.01}
    pa = {'0': 0.011, '1': 0.012}
    s = {'0': 0.013, '1': 0.014}
    gi = {'0': 0.015, '1': 0.016}
    gp = {'0': 0.017, '1': 0.018}
    gs = {'0': 0.019, '1': 0.02}
    gc = {'0': 0.021, '1': 0.022}
    model = get_model(age_enum=ages, init_comp=ic, _lambda=l, _v=v, _omega_n=on, _omega_v=ov, _e=e, _p_a=pa, _sigma=s,
                      _gamma_i=gi, _gamma_p=gp, _gamma_s=gs, _gamma_c=gc)

    for age in ages:
        print('@@@@@@@@@@@@@@@')
        print(age)
        print('***************')
        executor = Executor(model[age])
        values = model[age].get_values()
        print(values)

        for index in range(10):
            executor.simulate_step(index)
            values = model[age].get_values()
            print(values)
