def get_population(ages):
    area_age_popu = {}

    popu_file = open('popu.csv', encoding='utf8')
    popu_file.readline()
    for line in popu_file.readlines():
        if '|' in line:
            continue
        area = line.split(',')[1][1:-1]

        if area not in area_age_popu.keys():
            area_age_popu[area] = {}
            for age in ages:
                area_age_popu[area][age] = 0.0

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


from OHEI_base_area_age import get_ages

if __name__ == '__main__':
    df = get_population(get_ages(16))
    print(df['World'])
