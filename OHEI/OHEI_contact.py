import datetime as dt


def get_contact(ages):
    area_age_contact = {}
    file = open('external_datas/all.csv', encoding='utf8')
    line = file.readline().replace('\n', '').split(',')
    for item in line:
        area_iso = item[1:4]
        if area_iso not in area_age_contact.keys():
            area_age_contact[area_iso] = {}
            for age_from in ages:
                area_age_contact[area_iso][age_from] = {}
                for age_to in ages:
                    area_age_contact[area_iso][age_from][age_to] = {}

    for kind in ['home', 'others', 'work', 'school']:
        file = open('external_datas/' + kind + '.csv', encoding='utf8')
        lines = []
        for line in file.readlines():
            lines.append(line.replace('\n', '').split(','))
        for index in range(len(lines[0])):
            area_iso = lines[0][index][1:4]
            age_from = ages[index % 16]
            for age_to_index in range(len(ages)):
                age_to = ages[age_to_index]
                value = float(lines[age_to_index + 1][index])
                area_age_contact[area_iso][age_from][age_to][kind] = value

    return area_age_contact


def get_contact_modify(contact_origin, length, start_date: str, mobility, policy):
    contact_modify = {}
    for age_from in contact_origin.keys():
        contact_modify[age_from] = {}
        for age_to in contact_origin[age_from].keys():
            contact_modify[age_from][age_to] = []
            basic_contact = contact_origin[age_from][age_to]

            y = int(start_date[0:4])
            m = int(start_date[4:6])
            d = int(start_date[6:])
            ym = int(mobility['start_date'][0:4])
            mm = int(mobility['start_date'][4:6])
            dm = int(mobility['start_date'][6:])
            yp = int(policy['start_date'][0:4])
            mp = int(policy['start_date'][4:6])
            dp = int(policy['start_date'][6:])

            mobility_start_index = dt.datetime(y, m, d) - dt.datetime(ym, mm, dm)
            mobility_start_index = mobility_start_index.days
            policy_start_index = dt.datetime(y, m, d) - dt.datetime(yp, mp, dp)
            policy_start_index = policy_start_index.days

            for index in range(length):
                modify_value = basic_contact['home']
                if 'data' not in mobility.keys():
                    modify_value += basic_contact['others'] + basic_contact['work']
                else:
                    mobility_work = 1.0 + mobility['data']['workplaces'][index + mobility_start_index] * 0.01
                    modify_value += basic_contact['work'] * mobility_work
                    mobility_others = 1.0 + mobility['data']['retail_recreation'][index + mobility_start_index] * 0.01 + \
                                      mobility['data']['grocery_pharmacy'][index + mobility_start_index] * 0.01 + \
                                      mobility['data']['transit_stations'][index + mobility_start_index] * 0.01
                    modify_value += basic_contact['others'] * mobility_others
                if 'data' not in policy.keys():
                    modify_value += basic_contact['school']
                else:
                    policy_school = policy['data'][index + policy_start_index]
                    if policy_school == '0':
                        modify_value += basic_contact['school']
                    elif policy_school == '1':
                        modify_value += basic_contact['school'] * 0.5
                    elif policy_school == '2':
                        modify_value += basic_contact['school'] * 0.5
                    else:
                        pass
                contact_modify[age_from][age_to].append(modify_value)

    return contact_modify


from OHEI_base_area_age import get_ages

if __name__ == '__main__':
    df = get_contact(get_ages(16))
    print(df['AF']['15-19']['40-44'])
