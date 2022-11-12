from OHEI_base_area_age import get_ages, get_areas
from OHEI_init_population import get_population
from OHEI_contact import get_contact, get_contact_modify
from OHEI_mobility_policy import get_mobility, get_policy
from OHEI_GDP import get_gdp
from OHEI_vaccine_plan import get_vaccine_plan
from model import get_model
from executor.Executor import Executor
from json import load


def dataloader_OHEI_model(age_group=16):
    age_enum = get_ages(age_group_num=age_group)
    popu = get_population(age_enum)
    epi_non_area_time = load(open('settings/epi_non_time_area.json', encoding='utf8'))
    contact = get_contact(age_enum)
    init_vaccine = load(open('settings/init_vaccine.json', encoding='utf8'))
    mobility = get_mobility()
    policy = get_policy()
    gdp = get_gdp()
    return popu, epi_non_area_time, contact, init_vaccine, mobility, policy, gdp


def execute_OHEI_model(start_date, time_length, select_area, popu, epi_non_area_time, contact, mobility, policy,
                       init_vaccine, vacc_out, vacc_pri, gdp, age_group=16, verbose_load=False, verbose_modify=False,
                       verbose_simulation=False, simulation_disp=1):
    # load basic data
    age_enum = get_ages(age_group_num=age_group)
    areacode = get_areas()
    select_iso2 = None
    select_iso3 = None
    find_area = False
    for area_iso2 in areacode.keys():
        if areacode[area_iso2]['en'] == select_area:
            find_area = True
            select_iso2 = area_iso2
            select_iso3 = areacode[area_iso2]['iso3']
    if not find_area:
        print('Error: Select Area Invalid!')
        return None

    # load popu data
    if select_area not in popu.keys():
        print('Error: Population File Incomplete!')
        return None
    init_people = popu[select_area]
    if verbose_load:
        print(init_people)

    # load non_area_time params data
    if verbose_load:
        print(epi_non_area_time)

    # load contact data
    if select_iso3 not in contact.keys():
        print('Error: Contact File Incomplete!')
        return None
    contact_origin = contact[select_iso3]
    if verbose_load:
        print(contact_origin)

    # load init vaccine
    if verbose_load:
        print(init_vaccine)

    # load mobility/policy data
    mobility_origin = {}
    if select_iso2 not in mobility.keys():
        print('Warning: Mobility File Incomplete! Will use all 0.0 instead')
    else:
        mobility_origin = {'data': mobility[select_iso2]}
    mobility_origin['start_date'] = mobility['start_date']
    if verbose_load:
        print(mobility_origin)

    policy_origin = {}
    if select_iso3 not in policy.keys():
        print('Warning: Policy File Incomplete! Will use all 0.0 instead')
    else:
        policy_origin = {'data': policy[select_iso3]}
    policy_origin['start_date'] = policy['start_date']
    if verbose_load:
        print(policy_origin)

    # load GDP
    gdp_per = 0.0
    if select_iso3 not in gdp.keys():
        print('Warning: GDP File Incomplete! Will use all 0.0 instead')
    else:
        gdp_per = gdp[select_iso3]
    if verbose_load:
        print(gdp_per)

    # modify contact through mobility/policy
    contact_modify = get_contact_modify(contact_origin, time_length, start_date, mobility_origin, policy_origin)
    if verbose_modify:
        print(contact_modify)

    # modify(or more correct, calculate) init compartment values
    init_compartment_value = {}
    for age_i in age_enum:
        init = init_vaccine[age_i].copy()
        popu_sum = init_people[age_i]
        for comp in init.keys():
            init[comp] *= popu_sum / 10000.0
        init_compartment_value[age_i] = init

    # modify(or more correct, calculate) vaccine values
    vaccine_plan = get_vaccine_plan(age_enum, init_compartment_value, time_length, vacc_out, vacc_pri)
    if vaccine_plan is None:
        return None
    if verbose_modify:
        print(vaccine_plan)

    # create model
    enat = epi_non_area_time
    model = get_model(age_enum=age_enum, init_comp=init_compartment_value, _lambda=enat['zero'], _v=enat['zero'],
                      _omega_n=enat['omega_n'], _omega_v=enat['omega_v'], _e=enat['e'], _p_a=enat['p_a'],
                      _sigma=enat['sigma'], _gamma_i=enat['gamma_i'], _gamma_p=enat['gamma_p'],
                      _gamma_s=enat['gamma_s'], _gamma_c=enat['gamma_c'])

    # simulate model
    results = {}
    for age in age_enum:
        results[age] = {}
        for compartment in init_compartment_value[age].keys():
            results[age][compartment] = [init_compartment_value[age][compartment]]

    dailynew_eval = {}
    for age in age_enum:
        dailynew_eval[age] = {'E': [], 'Ic': []}

    for index in range(time_length):
        if verbose_simulation and index % simulation_disp == 0:
            print('days: ', index)

        for age_i in age_enum:
            executor = Executor(model[age_i])

            # cal lambda
            u_i = enat['u'][age_i]
            lambda_i = 0.0
            for age_j in age_enum:
                values = model[age_j].get_values()
                lambda_j = values['Ip'] + values['Ic'] + 0.5 * values['Is']
                popu_j = init_people[age_i]
                # lambda_i += lambda_j/popu_j * C_ijt
                lambda_i += contact_modify[age_i][age_j][index] * lambda_j / popu_j
            lambda_i *= u_i
            model[age_i].reset_parameters('lambda', lambda_i)
            model[age_i].reset_parameters('v', vaccine_plan[age_i][index])

            dailynew_eval_item = executor.simulate_step(index, ['E', 'Ic'])
            values = model[age_i].get_values()

            for compartment in values.keys():
                results[age_i][compartment].append(values[compartment])

            dailynew_eval[age_i]['E'].append(dailynew_eval_item['E'])
            dailynew_eval[age_i]['Ic'].append(dailynew_eval_item['Ic'])

            if verbose_simulation and index % simulation_disp == 0:
                print('ages: ', age_i, ' ', values)
    return results, dailynew_eval, vaccine_plan, gdp_per


if __name__ == '__main__':
    vacc_out_pool = ['less', 'normal', 'more', 'most']
    vacc_pri_pool = ['V+', 'V20', 'V60', 'V75']
    time_length = 180
    start_date = '20200801'
    select_area = 'United Kingdom'
    vacc_out = vacc_out_pool[1]
    vacc_pri = vacc_pri_pool[3]

    popu, epi1, contact, init_vacc, mobility, policy, gdp = dataloader_OHEI_model()
    results, dailynew, vp, gdp = execute_OHEI_model(start_date, time_length, select_area, popu, epi1, contact, mobility,
                                                    policy, init_vacc, vacc_out, vacc_pri, gdp)
    print(results)
