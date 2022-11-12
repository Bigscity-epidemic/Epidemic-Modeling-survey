def get_HC(death_age, gdp):
    LEdisc = {}
    for age in death_age.keys():
        age_start = float(age[:2].replace('-', ''))
        if age_start == 75:
            age_start = 80
        LEdisc[age] = 3.5 * (age_start ** 0.5)

    HC_age = {}
    HC_loss = 0.0
    for age in death_age.keys():
        death = 0.0

        for t in range(len(death_age[age])):
            death += death_age[age][t]

        HC_age[age] = LEdisc[age] * death * gdp
        HC_loss += HC_age[age]

    return HC_loss, HC_age
