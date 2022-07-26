import datetime as dt
from matplotlib import pyplot as plt
from matplotlib.font_manager import *
from math import log

myfont = FontProperties(fname='./simhei.ttf', size=14)
df = open('shanghai_daily.csv')
shanghai = []
for line in df.readlines():
    shanghai.append(float(line.replace('\n', '')))

t_range_subdt = [dt.date.today() + dt.timedelta(days=-60) + dt.timedelta(days=x) for x in
                 range(365)]
plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[0:59], shanghai[0:59], 'k.-')
plt.grid("True")
plt.legend(['上海日新增病例（确诊+无症状）'], prop=myfont)
plt.title(u'上海市疫情情况'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('日期')
plt.ylabel('病例数')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()
shanghai = []
shanghaiup = []
shanghaidown = []

df = open('_shanghai_Rtw5_lognormal_bfirst.csv')
df.readline()
df.readline()
for line in df.readlines():
    info = line.replace('\n', '').split(',')
    shanghai.append(float(info[1]))
    shanghaiup.append(float(info[2]))
    shanghaidown.append(float(info[3]))

plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[7:59], shanghai[0:52], 'o-', color='orange', label='上海实际再生数Rt')
plt.fill_between(t_range_subdt[7:59], shanghaidown, shanghaiup, color='wheat', alpha=0.5, label='95%置信区间')
plt.grid("True")
plt.legend(loc='upper left', prop=myfont, frameon=False)
plt.title(u'上海市疫情实际再生数'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('日期')
plt.ylabel('病例数')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()

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

plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[49:60], beijing[0:11], 'o-', color='orange', label='北京实际再生数Rt')
plt.fill_between(t_range_subdt[49:60], bd, bu, color='wheat', alpha=0.5, label='95%置信区间')
plt.grid("True")
plt.legend(loc='upper left', prop=myfont, frameon=False)
plt.title(u'北京市疫情实际再生数'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('日期')
plt.ylabel('病例数')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()
