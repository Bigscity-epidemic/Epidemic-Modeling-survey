from executor.Executor import Executor
from NPI.SEPIAR_graph import get_eqs
from compartment.Transfer import set_path_exp, set_path_parameters, init_compartment


def get_model(r0, hidden, infect, confirm, sym_ratio, ct_ratio, remove, income, contact_ratio, s0, i0):
    model = get_eqs()
    inf = 2147483647.0
    popu = s0 + i0

    set_path_exp(model, 'Income', 'I', 'income')
    set_path_parameters(model, 'Income', 'I', 'income', income)

    set_path_exp(model, 'S', 'E', 'betaI*I*S*n+betaP*P*S*n+betaasym*Is_ct*S*n+betaasym*A*S*n')
    set_path_parameters(model, 'S', 'E', 'betaI', 0.1 * r0)
    set_path_parameters(model, 'S', 'E', 'betaP', r0)
    set_path_parameters(model, 'S', 'E', 'betaasym', 0.2 * r0)
    set_path_parameters(model, 'S', 'E', 'n', 1.0 / popu)

    set_path_exp(model, 'E', 'P', 'gamma*E*nocontact')
    set_path_parameters(model, 'E', 'P', 'gamma', 1.0 / hidden)
    set_path_parameters(model, 'E', 'P', 'nocontact', 1.0 - contact_ratio)

    set_path_exp(model, 'E', 'Is', 'E*contact')
    set_path_parameters(model, 'E', 'Is', 'contact', contact_ratio)

    set_path_exp(model, 'P', 'I', 'alpha*P*sym*nocontact')
    set_path_parameters(model, 'P', 'I', 'alpha', 1.0 / infect)
    set_path_parameters(model, 'P', 'I', 'sym', sym_ratio)
    set_path_parameters(model, 'P', 'I', 'nocontact', 1.0 - contact_ratio)

    set_path_exp(model, 'P', 'A', 'alpha*P*asym*nocontact')
    set_path_parameters(model, 'P', 'A', 'alpha', 1.0 / infect)
    set_path_parameters(model, 'P', 'A', 'asym', 1.0 - sym_ratio)
    set_path_parameters(model, 'P', 'A', 'nocontact', 1.0 - contact_ratio)

    set_path_exp(model, 'P', 'Is', 'P*contact')
    set_path_parameters(model, 'P', 'Is', 'contact', contact_ratio)

    set_path_exp(model, 'I', 'Is', 'confirm*I*noct')
    set_path_parameters(model, 'I', 'Is', 'confirm', 1.0 / confirm)
    set_path_parameters(model, 'I', 'Is', 'noct', 1.0 - ct_ratio)

    set_path_exp(model, 'I', 'Is_ct', 'confirm*I*ct')
    set_path_parameters(model, 'I', 'Is_ct', 'confirm', 1.0 / confirm)
    set_path_parameters(model, 'I', 'Is_ct', 'ct', ct_ratio)

    set_path_exp(model, 'Is', 'R', 'remove*Is')
    set_path_parameters(model, 'Is', 'R', 'remove', 1.0 / remove)

    set_path_exp(model, 'Is_ct', 'R', 'remove_ct*Is_ct')
    set_path_parameters(model, 'Is_ct', 'R', 'remove_ct', 1.0 / remove)

    set_path_exp(model, 'A', 'R', 'remove_A*A')
    set_path_parameters(model, 'A', 'R', 'remove_A', 1.0 / remove)

    init_value = {'S': s0, 'E': 10.0 * i0, 'P': 3.0 * i0, 'I': i0, 'Is_ct': 0.0, 'Is': 0.0, 'A': 0.0, 'R': 0.0,
                  'Income': inf}
    init_compartment(model, init_value)
    return model


if __name__ == '__main__':
    # natural reproduce
    r0 = 6.0
    # days from E to P
    hidden = 7.0
    # days from P to I
    infect = 10.0
    # days from I to Is
    confirm = 3.0
    # ratio between I/A
    sym_ratio = 1.0
    # ratio between Is_ct/Is
    ct_ratio = 0.0
    # days from Is/A/Is_ct to R
    remove = 14.0
    # income infectious per day
    income = 0.3
    # ratio between Is/P
    contact_ratio = 0.0

    s0 = 1000000.0
    i0 = 1.0
    model = get_model(r0, hidden, infect, confirm, sym_ratio, ct_ratio, remove, income, contact_ratio, s0, i0)
    executor = Executor(model)
    values = model.get_values()
    print(values)

    for index in range(10):
        executor.simulate_step(index)
        values = model.get_values()
        print(values)
