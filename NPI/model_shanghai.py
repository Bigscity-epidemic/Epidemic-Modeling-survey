from NPI.base_NPI_model import get_model
from executor.Executor import Executor
from matplotlib import pyplot as plt
from matplotlib.font_manager import *
import datetime as dt
import json

settings = json.load(open('settings-shh.json', encoding='utf8'))
r0 = settings['r0']
infect = settings['患病者口罩比例']
suscept = settings['易感人群口罩比例']
print(r0)
r0 *= 1.0 - (infect * suscept * 0.99 + infect * (1.0 - suscept) * 0.6 + (1.0 - infect) * suscept * 0.6)
print(r0)
if settings['疫苗基础VEI'] != 0:
    modify = settings['疫苗VEI修正'].split(',')
    ratio = settings['疫苗接种率'].split(',')
    vei = settings['疫苗基础VEI']
    tmp = 0.0
    for i in range(4):
        tmp += float(modify[i]) * float(ratio[i])
    vei *= tmp
    r0 *= 1.0 - vei
print(r0)
hidden = settings['hidden_latency']
infect = settings['infect_latency']
confirm = settings['confirm_latency']
remove = settings['remove_latency']
sym_ratio = settings['base_sym_ratio']
if settings['无症状比例'] != 0.0:
    sym_ratio = 1.0 - settings['无症状比例']
ct_ratio = settings['base_ct_ratio']
contact_ratio = settings['base_contact_ratio']
income = settings['income_x']
s0 = settings['s0']

i0 = 1.0
model = get_model(r0, hidden, infect, confirm, sym_ratio, ct_ratio, remove, income, contact_ratio, s0, i0)
executor = Executor(model)
series = {}
values = model.get_values()
for compartment in values.keys():
    series[compartment] = [values[compartment]]

# 平均期望，在检测周期中均匀的出现初始病例
history = int(settings['高风险人群检测周期'] / 2.0)
future = 120

# 历史自由传播阶段
for index in range(history):
    executor.simulate_step(index)
    values = model.get_values()
    for compartment in values.keys():
        series[compartment].append(values[compartment])

# 发现第一例病例之后的阶段

## 综合社交距离响应等级
if settings['基础响应等级'] == 2:
    r0 *= 0.8
elif settings['基础响应等级'] == 3:
    r0 *= 0.05
else:
    r0 *= 1.0
model.reset_parameters('betaI', r0)
model.reset_parameters('betaP', 0.55 * r0)
model.reset_parameters('betact', 0.1 * r0)

## 快速核酸筛查（降低确诊标准）
ct_ratio = settings['核酸检测阳性判定']
model.reset_parameters('noct', 1.0 - ct_ratio)
model.reset_parameters('ct', ct_ratio)

## 密接隔离所需时长
contact_ratio = 1.0 / settings['密接隔离所需时长']
if settings['次密漏网比例'] != 0.0:
    contact_ratio *= (1.0 - settings['次密漏网比例'])
model.reset_parameters('nocontact', 1.0 - contact_ratio)
model.reset_parameters('contact', contact_ratio)

for index in range(future):

    ## 全民核酸检测
    if settings['全员核酸周期'] == 0:
        if str(index) in settings['全员核酸计划'].keys():
            model.reset_parameters('alpha', 0.1 / infect)
            tmp = model.name2compartments['I'].value * settings['全员核酸计划'][str(index)]
            model.name2compartments['I'].value -= tmp
            model.name2compartments['Is'].value += tmp

            tmp = model.name2compartments['P'].value * settings['全员核酸计划'][str(index)] * sym_ratio
            model.name2compartments['P'].value -= tmp
            model.name2compartments['Is'].value += tmp
    else:
        if index % settings['全员核酸周期'] == 0 and index != 0:
            tmp = model.name2compartments['I'].value
            model.name2compartments['I'].value -= tmp
            model.name2compartments['Is'].value += tmp

            tmp = model.name2compartments['P'].value * sym_ratio
            model.name2compartments['P'].value -= tmp
            model.name2compartments['Is'].value += tmp

    executor.simulate_step(index)
    values = model.get_values()
    for compartment in values.keys():
        series[compartment].append(values[compartment])

print(series)
ac = []
cfm = []
asymcfm = []
for i in range(len(series['S'])):
    ac.append(series['I'][i] + series['A'][i] + series['Is'][i] + series['R'][i])
    cfm.append(series['Is'][i] * 0.1 + series['I'][i] + series['R'][i] * 0.1)
    asymcfm.append(series['Is'][i] * 0.9 + series['A'][i] + series['R'][i] * 0.9)

myfont = FontProperties(fname='./simhei.ttf', size=14)
t_range_subdt = [dt.date.today() + dt.timedelta(days=-30) + dt.timedelta(days=-history) + dt.timedelta(days=x) for x in
                 range(365)]
disp_days = history + future - 1

truth = open('data_sh_since31.csv', encoding='utf8')
confirm_truth = [0, 0, 0]
infect_truth = [0, 0, 0]
sum_truth = [0, 0, 0]
for line in truth.readlines():
    confirm_truth.append(float(line.split(',')[1]))
    infect_truth.append(float(line.split(',')[2]))
    sum_truth.append(confirm_truth[-1] + infect_truth[-1])
"""
plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[1:][:disp_days], [asymcfm[i + 1] - asymcfm[i] for i in range(len(asymcfm) - 1)][:disp_days],
         'b+-')
plt.plot(t_range_subdt[:34][1:], infect_truth, 'k.-')
plt.grid("True")
plt.legend(["日新增无症状预测", '日新增无症状数'], prop=myfont)
plt.title(u'无症状'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('Date')
plt.ylabel('Case')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[0:][:disp_days + 1], [cfm[i + 1] - cfm[i] for i in range(len(cfm) - 1)], 'b+-')
plt.plot(t_range_subdt[:34][1:], confirm_truth, 'k.-')
plt.grid("True")
plt.legend(["日新增确诊数预测", '日新增确诊数'], prop=myfont)
plt.title(u'确诊'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('Date')
plt.ylabel('Case')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()
"""
plt.figure(figsize=(8, 6))
plt.yscale('log')
plt.plot(t_range_subdt[0:][:disp_days + 1], [ac[i + 1] - ac[i] for i in range(len(ac) - 1)], 'b+-')
plt.plot(t_range_subdt[:34][1:], sum_truth, 'k.-')
plt.grid("True")
plt.legend(["日新增无症状+确诊规模预测", '日新增无症状+确诊数'], prop=myfont)
plt.title(u'上海市无症状+确诊病例预测结果（对数坐标）'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('日期')
plt.ylabel('病例数')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[0:][:disp_days + 1], [ac[i + 1] - ac[i] for i in range(len(ac) - 1)], 'b+-')
plt.plot(t_range_subdt[:34][1:], sum_truth, 'k.-')
plt.grid("True")
plt.legend(["日新增无症状+确诊规模预测", '日新增无症状+确诊数'], prop=myfont)
plt.title(u'上海市无症状+确诊病例预测结果'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('日期')
plt.ylabel('病例数')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[0:][:disp_days + 1], [ac[i + 1] - ac[i] for i in range(len(ac) - 1)], 'b+-')
plt.plot(t_range_subdt[:34][1:], sum_truth, 'k.-')
plt.grid("True")
plt.legend(["Predict Results", 'Background Truth'], prop=myfont)
plt.title(u'The Result of Epidemic Mdel'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('Date')
plt.ylabel('Cases')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()
"""
plt.figure(figsize=(8, 6))
plt.plot(t_range_subdt[0:][:disp_days], ac[:disp_days], 'b+-')
plt.plot(t_range_subdt[:len(cfm)][0:], cfm, 'k.-')
plt.grid("True")
plt.legend(["累计感染数预测", '累计确诊数预测'], prop=myfont)
plt.title(u'上海'.format('某地区', '某时间'), FontProperties=myfont)
plt.xlabel('Date')
plt.ylabel('Case')
plt.gcf().autofmt_xdate()
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()
"""
