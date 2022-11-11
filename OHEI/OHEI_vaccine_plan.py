from json import dump
from OHEI_base_area_age import get_ages


def gen_init_ratio(ages):
    df = {}
    for age in ages:
        df[age] = {'S': 590.0, 'E': 5.0, 'Ip': 1.0, 'Ic': 1.0, 'R': 1.0, 'V': 9400.0, 'Ev': 1.0, 'Is': 1.0}
    dump(df, open('settings/init_vaccine.json', 'w', encoding='utf8'))


def get_vaccine_plan(init_compartment_value, time_length):
    vaccine_plan = {}
    return vaccine_plan


if __name__ == '__main__':
    gen_init_ratio(get_ages(16))
