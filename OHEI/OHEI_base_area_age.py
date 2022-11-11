def get_ages(age_group_num=16):
    ages = []
    for index in range(age_group_num):
        age_begin = index * 5
        age_end = age_begin + 4
        age_str = str(age_begin) + '-' + str(age_end)
        if age_begin == 75:
            age_str = '75+'
        ages.append(age_str)
    return ages


def get_areas():
    df = {}
    en_file = open('external_datas/country_en.csv', encoding='utf8')
    en_file.readline()
    for line in en_file.readlines():
        info = line.split(',')
        area_en = info[0]
        iso2 = info[1]
        iso3 = info[2]
        df[iso2] = {'en': area_en, 'iso3': iso3}
    zh_file = open('external_datas/country_zh.csv', encoding='utf8')
    zh_file.readline()
    for line in zh_file.readlines():
        iso2 = line[:2]
        area_zh = line[3:-1]
        df[iso2]['zh'] = area_zh
    return df


if __name__ == '__main__':
    print(get_areas())
