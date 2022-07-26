import datetime as dt

data = []
f1 = open('data_sh_since31.csv', encoding='utf8')
for line in f1.readlines():
    data.append(int(line.split(',')[-2]))

f2 = open('Shanghai_region_data_T.csv', encoding='utf8')
f2.readline()
sh = f2.readline().split(',')[1:]
for i in range(53):
    x = int(sh[2 * i])
    y = int(sh[2 * i + 1])
    data.append(x + y)
print(data)
results = open('_shanghai.csv', 'w', encoding='utf8')

start_date = dt.date(2022, 3, 1)
for item in data:
    results.write(start_date.strftime('%Y/%m/%d'))
    results.write(',')
    results.write(str(item))
    results.write('\n')
    start_date = start_date + dt.timedelta(1)
