from model import get_model
from executor.Executor import Executor
from matplotlib import pyplot as plt

# age_varing and area/vacc select
time_length = 365
age_group_num = 16


# make str age
def make_ages():
    ages = []
    for index in range(age_group_num):
        age_begin = index * 5
        age_end = age_begin + 4
        age_str = str(age_begin) + '-' + str(age_end)
        if age_begin == 75:
            age_str = '75+'
        ages.append(age_str)
    return ages


ages_enum = make_ages()


# fill age-varing, non-time-varing params
def fill_gamma_i_u(ages_enum_func):
    age_gamma_i_u_func = {}
    u = [0.3956736, 0.3956736, 0.3815349, 0.3815349, 0.7859512, 0.7859512, 0.8585759, 0.8585759, 0.7981468, 0.7981468,
         0.8166960, 0.8166960, 0.8784811, 0.8784811, 0.7383189, 0.7383189]
    gamma_i = [0.2904047, 0.2904047, 0.2070468, 0.2070468, 0.2676134, 0.2676134, 0.3284704, 0.3284704, 0.3979398,
               0.3979398, 0.4863355, 0.4863355, 0.6306967, 0.6306967, 0.6906705, 0.6906705]
    for index in range(age_group_num):
        age_gamma_i_u_func[ages_enum_func[index]] = {'gamma_i': gamma_i[index], 'u': u[index]}
        if index < 10:
            age_gamma_i_u_func[ages_enum_func[index]]['vac_enough'] = 0.7
        else:
            age_gamma_i_u_func[ages_enum_func[index]]['vac_enough'] = 0.9
    return age_gamma_i_u_func


age_gamma_i_u = fill_gamma_i_u(ages_enum_func=ages_enum)
print(age_gamma_i_u)


# make str area
def make_areas():
    # these areas are in OHEI origin paper, can use its contact metrics result
    area_str = " Albania, Armenia, Austria, Azerbaijan, Belarus, Belgium, Bosnia and Herzegovina, Bulgaria, " \
               "Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Georgia, Germany, Greece, " \
               "Hungary, Iceland, Ireland, Israel, Italy, Kazakhstan, Kyrgyzstan, Latvia, Lithuania, Luxembourg, " \
               "Malta, Montenegro, Netherlands, Norway, Poland, Portugal, Republic of Moldova, Romania, " \
               "Russian Federation, Serbia, Slovakia, Slovenia, Spain, Sweden, Switzerland, Tajikistan, " \
               "North Macedonia, Turkey, Turkmenistan, Ukraine, United Kingdom, Uzbekistan"
    areas = area_str.replace('\n', '').split(',')
    areas_no_space = []
    for item in areas:
        areas_no_space.append(item[1:])
    return areas_no_space


areas_enum = make_areas()


# fill popu
def fill_population(areas_enum_func, ages_enum_func, greedy_fill=True):
    area_age_popu = {}
    for area in areas_enum_func:
        area_age_popu[area] = {}
        for age in ages_enum_func:
            area_age_popu[area][age] = 0.0

    popu_file = open('popu.csv', encoding='utf8')
    popu_file.readline()
    for line in popu_file.readlines():
        if '|' in line:
            continue
        area = line.split(',')[1][1:-1]

        # if use greedy_fill, other area in popu.csv would also into areas_enum
        if area not in area_age_popu.keys():
            areas_enum_func.append('area')
            area_age_popu[area] = {}
            for age in ages_enum_func:
                area_age_popu[area][age] = 0.0

        if area in area_age_popu.keys():
            age = line.split(',')[2][1:-1]
            female = float(line.split(',')[3])
            male = float(line.split(',')[4])
            if age in area_age_popu[area].keys():
                area_age_popu[area][age] = round(male + female, 3)
            else:
                area_age_popu[area]['75+'] = round(male + female + area_age_popu[area]['75+'], 3)

    # add whole population
    for area in area_age_popu.keys():
        popu_sum = 0.0
        for age in area_age_popu[area].keys():
            popu_sum = round(popu_sum + area_age_popu[area][age], 3)
            area_age_popu[area][age] *= 10000.0
        area_age_popu[area]['popu'] = popu_sum * 10000.0

    return area_age_popu


# fill vacc ratio, may change later
def fill_vacc_init(area_popu_func):
    for area in area_popu_func.keys():
        area_popu_func[area]['vacc'] = 0.95
    return area_popu_func


area_popu = fill_population(areas_enum_func=areas_enum, ages_enum_func=ages_enum)
area_popu = fill_vacc_init(area_popu_func=area_popu)
print(area_popu)

# vaccine policy
vac_out_enum = ['R1', 'R2', 'R3', 'R4']
vac_pri_enum = ['V+', 'V20', 'V60', 'V75']
vac_out = {'R1': 1096, 'R2': 730, 'R3': 365, 'R4': 180}


def run_OHEI_model(ages, area, time_length, area_select, vac_select, vac_out, disp_interval=7):
    # gen population/non-time parameters
    init_compartment_value = {}
    for age in ages.keys():
        init = {'S': 9990.0, 'E': 5.0, 'Ip': 1.0, 'Ic': 1.0, 'R': 1.0, 'V': 0.0, 'Ev': 1.0, 'Is': 1.0}
        init['V'] = init['S'] * area[area_select]['vacc']
        init['S'] -= init['V']

        popu_sum = area[area_select][age]
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
        _omega_n[age] = 1.0 / 1096.0
        _omega_v[age] = 1.0 / 365.0

    ## e \equiv 0.95,pa \equiv 0.95
    _e = {}
    _p_a = {}
    for age in ages.keys():
        _e[age] = 0.95
        _p_a[age] = 0.95

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
        popu_age[age] = area[area_select][age]

    dailynew_confirm = []

    for index in range(time_length):
        newconf = 0.0
        if index % disp_interval == 0:
            print('days: ', index)
        # cal v
        ## upd vaccined
        for age in ages.keys():
            popu_age[age] = area[area_select][age]
            vacc_age[age] = model[age].get_values()['V']

        ## cal today vaccine
        vac_age_today = {}
        today_vaccine = area[area_select]['popu'] / vac_out[vac_select[0]]

        for age in ages.keys():
            vac_age_today[age] = 100000.0

        for age in vac_age_today.keys():
            vac_age_today[age] = int(vac_age_today[age])
            vac_age_today[age] = float(vac_age_today[age])
        if index % disp_interval == 0:
            print('Vaccine Use Today: ', vac_age_today)

        for age in ages.keys():
            executor = Executor(model[age])

            # cal lambda
            u_i = ages[age]['u']
            c_ijt = 0.03
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
            if index % disp_interval == 0:
                print('ages: ', age, ' ', values)
        dailynew_confirm.append(newconf)

    plt.plot(dailynew_confirm)
    plt.show()


run_OHEI_model(ages=age_gamma_i_u, area=area_popu, time_length=time_length, area_select='China',
               vac_select=[vac_out_enum[2], vac_pri_enum[3]], vac_out=vac_out, disp_interval=30)
