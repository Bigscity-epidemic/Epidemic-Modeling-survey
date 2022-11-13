def get_cQALY(death_age, infected_age, vaccine_plan):
    adjQALEdisc = {}
    for age in death_age.keys():
        age_start = float(age[:2].replace('-', ''))
        if age_start == 75:
            age_start = 80
        adjQALEdisc[age] = 3 * ((100 - age_start) ** 0.5)
    mean_QALYloss_symptom = 0.0307
    mean_QALYloss_AEFI = 1.0
    AEFI_probability = 0.5

    cQALY_age = {}
    cQALY_loss = 0.0

    for age in death_age.keys():
        death = 0.0
        infect = 0.0

        for t in range(len(death_age[age])):
            death += death_age[age][t]
            infect += infected_age[age][t]

        vacc = 0.0
        for t in range(len(vaccine_plan[age])):
            vacc += vaccine_plan[age][t]

        QALE_loss = adjQALEdisc[age] * death
        sym_loss = mean_QALYloss_symptom * infect
        vacc_loss = vacc * mean_QALYloss_AEFI * AEFI_probability

        cQALY_age[age] = QALE_loss + sym_loss + vacc_loss
        cQALY_loss += cQALY_age[age]

    return cQALY_loss, cQALY_age
