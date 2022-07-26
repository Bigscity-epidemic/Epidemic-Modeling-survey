from executor.Executor import Executor
from MERE.SPIAHDR_graph import get_eqs
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment


def get_model(r0, confirm, remove, hospital, icu, sym_ratio, recover_ratio, severe_ratio, death_ratio, s0, i0):
    model = get_eqs()
    popu = s0 + i0

    set_path_exp(model, 'S', 'P', 'beta*P*S*n+betaA*A*S*n')
    set_path_parameters(model, 'S', 'P', 'beta', r0)
    set_path_parameters(model, 'S', 'P', 'betaA', 0.1 * r0)
    set_path_parameters(model, 'S', 'P', 'n', 1.0 / popu)

    set_path_exp(model, 'P', 'I', 'alpha*P*sym')
    set_path_parameters(model, 'P', 'I', 'alpha', 1.0 / confirm)
    set_path_parameters(model, 'P', 'I', 'sym', sym_ratio)

    set_path_exp(model, 'P', 'A', 'alpha*P*asym')
    set_path_parameters(model, 'P', 'A', 'alpha', 1.0 / confirm)
    set_path_parameters(model, 'P', 'A', 'asym', 1.0 - sym_ratio)

    set_path_exp(model, 'I', 'R', 'gamma*I*recover')
    set_path_parameters(model, 'I', 'R', 'gamma', 1.0 / remove)
    set_path_parameters(model, 'I', 'R', 'recover', recover_ratio)

    set_path_exp(model, 'I', 'H', 'gamma*I*hospital')
    set_path_parameters(model, 'I', 'H', 'gamma', 1.0 / remove)
    set_path_parameters(model, 'I', 'H', 'hospital', 1.0 - recover_ratio)

    set_path_exp(model, 'A', 'R', 'gamma*A')
    set_path_parameters(model, 'A', 'R', 'gamma', 1.0 / remove)

    set_path_exp(model, 'H', 'R', 'hos*H*normal')
    set_path_parameters(model, 'H', 'R', 'hos', 1.0 / hospital)
    set_path_parameters(model, 'H', 'R', 'normal', 1.0 - severe_ratio)

    set_path_exp(model, 'H', 'Icu', 'hos*H*severe')
    set_path_parameters(model, 'H', 'Icu', 'hos', 1.0 / hospital)
    set_path_parameters(model, 'H', 'Icu', 'severe', severe_ratio)

    set_path_exp(model, 'Icu', 'D', 'icu*Icu*death')
    set_path_parameters(model, 'Icu', 'D', 'icu', 1.0 / icu)
    set_path_parameters(model, 'Icu', 'D', 'death', death_ratio)

    set_path_exp(model, 'Icu', 'H', 'icu*Icu*health')
    set_path_parameters(model, 'Icu', 'H', 'icu', 1.0 / icu)
    set_path_parameters(model, 'Icu', 'H', 'health', 1.0 - death_ratio)

    init_value = {'S': s0, 'P': 2.0 * i0, 'I': i0, 'A': 0, 'H': 0, 'R': 0, 'D': 0, 'Icu': 0}
    init_compartment(model, init_value)
    return model


if __name__ == '__main__':
    # natural reproduce
    r0 = 1.0
    # days from P to I
    confirm = 3.0
    # days from I/A to R
    remove = 7.0
    # ratio between I/A
    sym_ratio = 0.1
    # ratio between R/H
    recover_ratio = 0.7
    # days in hospital average
    hospital = 8.0
    # days in icu average
    icu = 15.0
    # severe and death
    severe_ratio = 0.1
    death_ratio = 0.2

    s0 = 1000000.0
    i0 = 1.0
    model = get_model(r0, confirm, remove, hospital, icu, sym_ratio, recover_ratio, severe_ratio, death_ratio, s0, i0)
    executor = Executor(model)
    values = model.get_values()
    print(values)

    for index in range(10):
        executor.simulate_step(index)
        values = model.get_values()
        print(values)

    set_path_parameters(model, 'S', 'E', 'beta', 0.3)
    set_path_parameters(model, 'S', 'E', 'popu', 1.0 / 1000000)
    set_path_parameters(model, 'E', 'I', 'alpha', 0.14)
    set_path_parameters(model, 'I', 'R', 'gamma', 0.2)

    set_path_exp(model, 'S', 'E', 'beta*S*I*popu')
    set_path_exp(model, 'E', 'I', 'alpha*E')
    set_path_exp(model, 'I', 'R', 'gamma*I')
