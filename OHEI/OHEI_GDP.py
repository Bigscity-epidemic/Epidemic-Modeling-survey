def get_gdp():
    area_gdp = {}
    df = open('external_datas/gdp.csv', encoding='utf8')
    for i in range(5):
        df.readline()
    for line in df.readlines():
        info = line.replace('\n', '').split(',')
        iso3 = info[1][1:-1]
        index = len(info) - 1
        while True:
            if index == 3:
                area_gdp[iso3] = 0.0
                break
            gdp_str = info[index]
            if gdp_str != '\"\"' and gdp_str != '':
                area_gdp[iso3] = float(gdp_str[1:-1])
                break
            index -= 1
    return area_gdp


if __name__ == '__main__':
    print(get_gdp())
