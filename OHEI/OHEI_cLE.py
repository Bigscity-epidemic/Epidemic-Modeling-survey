def get_cLE(death_age):
    cLE_age = {}
    cLE_loss = 0.0
    for age in death_age.keys():
        cLE_age[age] = 0.0

        for item in death_age[age]:
            cLE_age[age] += item

        age_start = float(age[:2].replace('-', ''))
        if age_start == 75:
            age_start = 80

        cLE_age[age] *= 100 - (age_start + 2)
        cLE_loss += cLE_age[age]
    return cLE_loss, cLE_age
