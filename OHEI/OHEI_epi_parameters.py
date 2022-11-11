from json import dump
from OHEI_base_area_age import get_ages


def gen_epi_par(ages):
    _omega_n = {}
    _omega_v = {}
    for age in ages:
        _omega_n[age] = 1.0 / 1096.0
        _omega_v[age] = 1.0 / 365.0

    _e = {}
    _p_a = {}
    for age in ages:
        _e[age] = 0.95
        _p_a[age] = 0.95

    _sigma = {}
    _gamma_p = {}
    _gamma_s = {}
    _gamma_c = {}
    for age in ages:
        _sigma[age] = 1.0 / 2.5
        _gamma_p[age] = 1.0 / 1.5
        _gamma_s[age] = 1.0 / 5.0
        _gamma_c[age] = 1.0 / 3.5

    _zero = {}
    for age in ages:
        _zero[age] = 0.0

    u = [0.3956736, 0.3956736, 0.3815349, 0.3815349, 0.7859512, 0.7859512, 0.8585759, 0.8585759, 0.7981468, 0.7981468,
         0.8166960, 0.8166960, 0.8784811, 0.8784811, 0.7383189, 0.7383189]
    gamma_i = [0.2904047, 0.2904047, 0.2070468, 0.2070468, 0.2676134, 0.2676134, 0.3284704, 0.3284704, 0.3979398,
               0.3979398, 0.4863355, 0.4863355, 0.6306967, 0.6306967, 0.6906705, 0.6906705]

    u_age = {}
    gamma_i_age = {}
    index = 0
    for age in ages:
        u_age[age] = u[index]
        gamma_i_age[age] = gamma_i[index]
        index += 1
    df = {'omega_n': _omega_n, 'omega_v': _omega_v, 'e': _e, 'p_a': _p_a, 'sigma': _sigma, 'u': u_age, 'zero': _zero,
          'gamma_i': gamma_i_age, 'gamma_p': _gamma_p, 'gamma_s': _gamma_s, 'gamma_c': _gamma_c}
    dump(df, open('settings/epi_non_time_area.json', 'w', encoding='utf8'))


if __name__ == '__main__':
    gen_epi_par(get_ages(16))
