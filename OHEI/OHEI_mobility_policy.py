def get_mobility():
    area_mobility = {'start_date': '20200214'}
    mobility_file = open('external_datas/mobility.csv', encoding='utf8')
    mobility_file.readline()
    for line in mobility_file.readlines():
        info = line.replace('\n', '').split(',')
        area = info[0]
        if area not in area_mobility.keys():
            area_mobility[area] = {'retail_recreation': [0.0], 'grocery_pharmacy': [0.0], 'parks': [0.0],
                                   'transit_stations': [0.0], 'workplaces': [0.0], 'residential': [0.0]}
        if info[-6] == '':
            area_mobility[area]['retail_recreation'].append(area_mobility[area]['retail_recreation'][-1])
        else:
            area_mobility[area]['retail_recreation'].append(float(info[-6]))
        if info[-5] == '':
            area_mobility[area]['grocery_pharmacy'].append(area_mobility[area]['grocery_pharmacy'][-1])
        else:
            area_mobility[area]['grocery_pharmacy'].append(float(info[-5]))
        if info[-4] == '':
            area_mobility[area]['parks'].append(area_mobility[area]['parks'][-1])
        else:
            area_mobility[area]['parks'].append(float(info[-4]))
        if info[-3] == '':
            area_mobility[area]['transit_stations'].append(area_mobility[area]['transit_stations'][-1])
        else:
            area_mobility[area]['transit_stations'].append(float(info[-3]))
        if info[-2] == '':
            area_mobility[area]['workplaces'].append(area_mobility[area]['workplaces'][-1])
        else:
            area_mobility[area]['workplaces'].append(float(info[-2]))
        if info[-1] == '':
            area_mobility[area]['residential'].append(area_mobility[area]['residential'][-1])
        else:
            area_mobility[area]['residential'].append(float(info[-1]))
    return area_mobility


def get_policy():
    area_policy = {'start_date': '20191230'}
    policy_file = open('external_datas/policy.csv', encoding='utf8')
    policy_file.readline()
    for line in policy_file.readlines():
        area = line.split(',')[1]
        value = line.split(',')[6]
        if area not in area_policy.keys():
            area_policy[area] = ['0']
        if value == '':
            area_policy[area].append(area_policy[area][-1])
        else:
            area_policy[area].append(value[0])
    return area_policy


if __name__ == '__main__':
    df = get_policy()
    print(df['ABW'])
