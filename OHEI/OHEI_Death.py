from scipy.stats import gamma


def get_death(model_results):
    IFRj = {}
    for age in model_results.keys():
        age_start = float(age[:2].replace('-', ''))
        if age_start == 75:
            age_start = 80
        right_side = -3.27 + 0.0524 * (age_start + 2)
        IFRj[age] = 10 ** (right_side - 2)

    death_age = {}
    death_whole = 0.0
    for age in model_results.keys():
        death_age[age] = []
        for t in range(len(model_results[age]['E'])):
            death_jt = 0.0
            for d in range(1, 60):
                E_index = t - d
                if E_index < 0:
                    continue
                death_djt = model_results[age]['E'][E_index] * IFRj[age] * gamma.pdf(d, 26, 5)
                death_jt += death_djt
            death_age[age].append(death_jt)
            death_whole += death_jt

    return death_whole,death_age


if __name__ == '__main__':
    x = []
    for d in range(60):
        x.append(d + 1)
    y = gamma.pdf(x, 26, 5)
    print(y)
