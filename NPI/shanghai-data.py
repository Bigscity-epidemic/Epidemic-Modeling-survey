df = open('daily_report_by_address.csv')
shanghai = []
df.readline()
line = df.readline().replace(',\n', '')
info = line.split(',')
for item in info[1:]:
    shanghai.append(float(item))
for line in df.readlines():
    info = line.replace('\n', '').split(',')
    for i in range(1, len(info)):
        shanghai[i - 1] += float(info[i])
result = open('shanghai_daily.csv', 'w', encoding='utf8')
for item in shanghai:
    result.write(str(item))
    result.write('\n')
