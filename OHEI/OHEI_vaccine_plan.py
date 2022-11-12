from json import dump
from OHEI_base_area_age import get_ages


def gen_init_ratio(ages):
    df = {}
    for age in ages:
        df[age] = {'S': 590.0, 'E': 5.0, 'Ip': 1.0, 'Ic': 1.0, 'R': 1.0, 'V': 9400.0, 'Ev': 1.0, 'Is': 1.0}
    dump(df, open('settings/init_vaccine.json', 'w', encoding='utf8'))


def get_vaccine_plan(age_enum, init_compartment_value, time_length, vacc_out, vacc_pri):
    vaccine_plan = {}

    # cal population
    popu_whole = 0.0
    popu_age = {}
    popu_rest = {}
    all_inject = False
    for age in init_compartment_value.keys():
        popu_age[age] = 0.0
        for compartment in init_compartment_value[age].keys():
            popu_whole += init_compartment_value[age][compartment]
            popu_age[age] += init_compartment_value[age][compartment]
        popu_rest[age] = init_compartment_value[age]['S']
        vaccine_plan[age] = []

    # cal vaccine whole amount by population
    vacc_whole = 0.0
    if vacc_out == 'less':
        vacc_whole = popu_whole * time_length / 1096.0
    elif vacc_out == 'normal':
        vacc_whole = popu_whole * time_length / 730.0
    elif vacc_out == 'more':
        vacc_whole = popu_whole * time_length / 365.0
    elif vacc_out == 'most':
        vacc_whole = popu_whole * time_length / 180.0
    else:
        print('Error: Invalid Vaccine Carryout Policy!')
        return None

    # cal pri number, 0 max, 8 min, 9 means no reject
    pri = []
    if vacc_pri == 'V+':
        pri = [9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif vacc_pri == 'V20':
        pri = [9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    elif vacc_pri == 'V60':
        pri = [9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    elif vacc_pri == 'V75':
        pri = [9, 9, 9, 9, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0]
    else:
        print('Error: Invalid Vaccine Prior Policy!')
        return None

    # cal vac plan
    for index in range(time_length):
        vacc_today = vacc_whole / (time_length - index)
        vacc_whole -= vacc_today
        plan_today = {}
        for age in age_enum:
            plan_today[age] = 0.0

        # inject like V+
        if all_inject:
            for age in age_enum[4:]:
                plan_today[age] = vacc_today * popu_age[age] / popu_whole

        # continue to inject with vacc_pri
        else:
            for pri_now in range(10):
                if pri_now == 9:
                    all_inject = True
                    break
                # ages should inject
                inject_indexs = []
                for age_index in range(len(age_enum)):
                    if pri_now == pri[age_index] and popu_rest[age_enum[age_index]] > 0.0:
                        inject_indexs.append(age_index)

                # all people at this pri is injected
                if len(inject_indexs) == 0:
                    continue

                # inject these people
                for age_index in inject_indexs:
                    vacc_inject = vacc_today / len(inject_indexs)
                    popu_rest[age_enum[age_index]] -= vacc_inject
                    plan_today[age_enum[age_index]] = vacc_inject
                break

        for age in age_enum:
            vaccine_plan[age].append(plan_today[age])

    return vaccine_plan


if __name__ == '__main__':
    gen_init_ratio(get_ages(16))
