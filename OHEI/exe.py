from model import get_model
from executor.Executor import Executor
from matplotlib import pyplot as plt

# age_varing and area/vacc select
time_length = 720
ages = {'0-19': {'gamma_i': 0.21, 'u': 0.48, 'vac_enough': 0.7},
        '20-59': {'gamma_i': 0.21, 'u': 0.38, 'vac_enough': 0.7},
        '60-74': {'gamma_i': 0.4, 'u': 0.58, 'vac_enough': 0.9},
        '75+': {'gamma_i': 0.7, 'u': 0.88, 'vac_enough': 0.9}}
area = {'England': {'popu': 67900000, '0-19': 0.173, '20-59': 0.592, '60-74': 0.145, '75+': 0.09, 'vacc': 0.2},
        'France': {'popu': 66400000, '0-19': 0.173, '20-59': 0.592, '60-74': 0.145, '75+': 0.09, 'vacc': 0.2}}

vac_out = {'R1': 1096, 'R2': 730, 'R3': 365, 'R4': 180}
vac_pri = ['V+', 'V20', 'V60', 'V75']

area_select = 'England'
vac_select = ['R2', 'V+']

# gen population/non-time parameters
init_compartment_value = {}
for age in ages.keys():
    init = {'S': 9860.0, 'E': 5.0, 'Ip': 10.0, 'Ic': 10.0, 'R': 100.0, 'V': 0.0, 'Ev': 5.0, 'Is': 10.0}
    init['V'] = init['S'] * area[area_select]['vacc']
    init['S'] -= init['V']
    popu_sum = area[area_select]['popu'] * area[area_select][age]
    for comp in init.keys():
        init[comp] *= popu_sum / 10000.0
    init_compartment_value[age] = init

## lambda/v is time-varing
_lambda = {}
_v = {}
for age in ages.keys():
    _lambda[age] = 0.0
    _v[age] = 0.0

## omega is non-time, 1/3 year
_omega_n = {}
_omega_v = {}
for age in ages.keys():
    _omega_n[age] = 1.0 / 180.0
    _omega_v[age] = 1.0 / 365.0

## e \equiv 0.95,pa \equiv 0.95
_e = {}
_p_a = {}
for age in ages.keys():
    _e[age] = 0.8
    _p_a[age] = 0.8

## use mean to replace Gamma distribution
_sigma = {}
_gamma_p = {}
_gamma_s = {}
_gamma_c = {}
for age in ages.keys():
    _sigma[age] = 1.0 / 2.5
    _gamma_p[age] = 1.0 / 1.5
    _gamma_s[age] = 1.0 / 5.0
    _gamma_c[age] = 1.0 / 3.5

## gamma_i is non-time but age varing
_gamma_i = {}
for age in ages.keys():
    _gamma_i[age] = ages[age]['gamma_i']

model = get_model(age_enum=list(ages.keys()), init_comp=init_compartment_value, _lambda=_lambda, _v=_v,
                  _omega_n=_omega_n, _omega_v=_omega_v, _e=_e, _p_a=_p_a, _sigma=_sigma, _gamma_i=_gamma_i,
                  _gamma_p=_gamma_p, _gamma_s=_gamma_s, _gamma_c=_gamma_c)

# cal vacc for future calculation
vacc_age = {}
popu_age = {}
for age in ages.keys():
    popu_age[age] = area[area_select]['popu'] * area[area_select][age]

dailynew_confirm = []

for index in range(time_length):
    newconf = 0.0
    if index % 7 == 0:
        print('days: ', index)
    # cal v
    ## upd vaccined
    for age in ages.keys():
        popu_age[age] = area[area_select]['popu'] * area[area_select][age]
        vacc_age[age] = model[age].get_values()['V']

    ## cal today vaccine
    vac_age_today = {}
    today_vaccine = area[area_select]['popu'] / vac_out[vac_select[0]]

    ## 4 vac_pri
    if vac_select[1] == 'V+':
        for age in ages.keys():
            vac_tmp = today_vaccine * popu_age[age] / area[area_select]['popu']
            vac_age_today[age] = vac_tmp

    elif vac_select[1] == 'V20':
        for age in ages.keys():
            vac_age_today[age] = 0.0

        if vacc_age['20-59'] + today_vaccine < popu_age['20-59'] * ages['20-59']['vac_enough']:
            vac_age_today['20-59'] = today_vaccine
        else:
            vac_tmp = popu_age['20-59'] * ages['20-59']['vac_enough'] - vacc_age['20-59']
            vac_age_today['20-59'] = vac_tmp
            vac_rest = today_vaccine - vac_tmp
            for age in ages.keys():
                if age != '20-59':
                    vac_tmp = vac_rest * popu_age[age] / area[area_select]['popu']
                    vac_age_today[age] = vac_tmp

    elif vac_select[1] == 'V60':
        for age in ages.keys():
            vac_age_today[age] = 0.0

        if vacc_age['60-74'] + today_vaccine < popu_age['60-74'] * ages['60-74']['vac_enough']:
            vac_age_today['60-74'] = today_vaccine
        else:
            vac_tmp = popu_age['60-74'] * ages['60-74']['vac_enough'] - vacc_age['60-74']
            vac_age_today['60-74'] = vac_tmp
            vac_rest = today_vaccine - vac_tmp
            for age in ages.keys():
                if age != '60-74':
                    vac_tmp = vac_rest * popu_age[age] / area[area_select]['popu']
                    vac_age_today[age] = vac_tmp

    elif vac_select[1] == 'V75':
        for age in ages.keys():
            vac_age_today[age] = 0.0

        if vacc_age['75+'] + today_vaccine < popu_age['75+'] * ages['75+']['vac_enough']:
            vac_age_today['75+'] = today_vaccine
        else:
            vac_tmp = popu_age['75+'] * ages['75+']['vac_enough'] - vacc_age['75+']
            vac_age_today['75+'] = vac_tmp
            vac_rest = today_vaccine - vac_tmp
            for age in ages.keys():
                if age != '75+':
                    vac_tmp = vac_rest * popu_age[age] / area[area_select]['popu']
                    vac_age_today[age] = vac_tmp
    else:
        print('Invalid Vaccine Prior Policy')
        exit('1')

    for age in vac_age_today.keys():
        vac_age_today[age] = int(vac_age_today[age])
        vac_age_today[age] = float(vac_age_today[age])
    if index % 7 == 0:
        print('Vaccine Use Today: ', vac_age_today)

    for age in ages.keys():
        executor = Executor(model[age])

        # cal lambda
        u_i = ages[age]['u']
        c_ijt = 0.3
        lambda_i = 0.0
        for age_j in ages.keys():
            values = model[age_j].get_values()
            lambda_j = values['Ip'] + values['Ic'] + 0.5 * values['Is']
            popu_j = 0.0
            # lambda_j = upper, popu_j =lower
            for comp in values.keys():
                popu_j += values[comp]
            # lambda_i += lambda_j * C_ijt
            lambda_i += c_ijt * lambda_j / popu_j
        lambda_i *= u_i
        model[age].reset_parameters('lambda', lambda_i)

        # upd vacc
        model[age].reset_parameters('v', vac_age_today[age])

        # cal dailynew
        newconf += model[age].get_values()['S'] * lambda_i
        newconf += model[age].get_values()['V'] * lambda_i * 0.64

        executor.simulate_step(index)
        values = model[age].get_values()
        if index % 7 == 0:
            print('ages: ', age, ' ', values)
    dailynew_confirm.append(newconf)

plt.plot(dailynew_confirm[100:])
plt.show()
