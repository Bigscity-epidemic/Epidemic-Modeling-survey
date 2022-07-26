import datetime as dt
from matplotlib import pyplot as plt
from matplotlib.font_manager import *
from math import log

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.sans-serif']=['SimHei']#显示中文标签
plt.rcParams['axes.unicode_minus']=False
from matplotlib.font_manager import *
myfont = FontProperties(fname='simhei.ttf', size=14)

def cal_r0(series):
    t = 3.0
    tg = 8.4
    p = 0.255
    r = []
    result = []
    last = 1.0
    for item in series:
        r.append(log(float(item + last)) / t)
        t += 1.0
        result.append(1 + r[-1] * tg + p * (1 - p) * (r[-1] * r[-1] * tg * tg))
        last += item
    return result


myfont = FontProperties(fname='./simhei.ttf', size=14)
df = open('data_sh_since31.csv')
shanghai = []
shenzhen = []
for line in df.readlines():
    info = line.split(',')
    shanghai.append(int(info[-2]))
    shenzhen.append(int(info[-1].replace('\n', '')))
print(shenzhen, shanghai)
print(cal_r0(shenzhen))
t_range_subdt = [dt.date.today() + dt.timedelta(days=-69) + dt.timedelta(days=x) for x in
                 range(365)]
plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[0:21], shenzhen[0:21], 'b+-')
plt.plot(t_range_subdt[0:21], shanghai[0:21], 'k.-')
plt.grid("True")
plt.legend(["深圳日新增病例（确诊+无症状）", '上海日新增病例（确诊+无症状）'], prop=myfont)
plt.title(u'上海市深圳市疫情情况对比'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('日期')
plt.ylabel('病例数')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()

shanghai = []
shanghaiup = []
shanghaidown = []
shenzhen = []
shenzhenup = []
shenzhendown = []
df = open('_shanghai_Rtw5_lognormal_bfirst.csv')
df.readline()
df.readline()
for line in df.readlines():
    info = line.replace('\n', '').split(',')
    shanghai.append(float(info[1]))
    shanghaiup.append(float(info[2]))
    shanghaidown.append(float(info[3]))

df = open('_shenzhen_Rtw5_lognormal_bfirst.csv')
df.readline()
df.readline()
for line in df.readlines():
    info = line.replace('\n', '').split(',')
    shenzhen.append(float(info[1]))
    shenzhenup.append(float(info[2]))
    shenzhendown.append(float(info[3]))

beijing = []
bu = []
bd = []

df = open('_beijing_Rtw5_lognormal_bfirst.csv')
df.readline()
df.readline()
for line in df.readlines():
    info = line.replace('\n', '').split(',')
    beijing.append(float(info[1]))
    bu.append(float(info[2]))
    bd.append(float(info[3]))

plt.figure(figsize=(7, 5))
plt.plot(t_range_subdt[12:64], shanghai[0:], 'o-', color='orange', label = '上海实际再生数Rt')
plt.fill_between(t_range_subdt[12:64], shanghaidown[0:], shanghaiup[0:], color='wheat', alpha=0.5, label='95%置信区间')
plt.plot(t_range_subdt[12:35], shenzhen[0:], 'o-', color='blue', label = '深圳实际再生数Rt')
plt.fill_between(t_range_subdt[12:35], shenzhendown[0:], shenzhenup[0:], color='lightskyblue', alpha=0.5, label='95%置信区间')
#plt.annotate('3.14深圳封城',size=14, xy=(t_range_subdt[12], 3.0), xytext=(t_range_subdt[8], 5.0), arrowprops=dict(arrowstyle="->", color="r", hatch='*',))
plt.grid("True")
ax = plt.gca()
data_format=mpl.dates.DateFormatter('%m-%d')
ax.xaxis.set_major_formatter(data_format)
plt.legend(loc = 'upper right', prop=myfont, frameon = False)
#plt.title(u'上海深圳疫情情况对比'.format('某地区', '某时间'), FontProperties=myfont)
#plt.xlabel('date')
plt.ylabel('实际再生数Rt',size=14)
plt.gcf().autofmt_xdate()
plt.savefig('shanghaishenzhen.jpg', dpi=300, bbox_inches='tight')
plt.show()


df = open('_beijing_Rtw5_lognormal_bfirst.csv')
df.readline()
df.readline()
for line in df.readlines():
    info = line.replace('\n', '').split(',')
    beijing.append(float(info[1]))
    bu.append(float(info[2]))
    bd.append(float(info[3]))
print(beijing)

plt.figure(figsize=(10, 5))
t_range_subdt=[]
for i in range(60):t_range_subdt.append(i+1)
plt.plot(t_range_subdt[0:23], shanghai[21:44], 'o-', color='orange', label = '上海实际再生数Rt')
plt.fill_between(t_range_subdt[0:23], shanghaidown[21:44], shanghaiup[21:44], color='wheat', alpha=0.5, label='95%置信区间')
plt.plot(t_range_subdt[0:18], shenzhen[4:22], 'o-', color='blue', label = '深圳实际再生数Rt')
plt.fill_between(t_range_subdt[0:18], shenzhendown[4:22], shenzhenup[4:22], color='lightskyblue', alpha=0.5, label='95%置信区间')

plt.plot(t_range_subdt[0:28], beijing[3:31], 'o-', color='green', label = '北京实际再生数Rt')
plt.fill_between(t_range_subdt[0:28], bd[3:31], bu[3:31], color='green', alpha=0.5, label='95%置信区间')

plt.grid("True")
plt.legend(loc = 'upper right', prop=myfont, frameon = False)
#plt.title(u'北、上、深疫情情况对比'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('封城或采取全面措施后的天数',size=14)
plt.ylabel('实际再生数Rt',size=14)
plt.savefig('beijingshanghaishenzhen.jpg', dpi=300, bbox_inches='tight')
plt.show()
