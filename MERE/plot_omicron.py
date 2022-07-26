from matplotlib import pyplot as plt
from matplotlib.font_manager import *

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.font_manager import *

myfont = FontProperties(fname='simhei.ttf', size=14)
myfont2 = FontProperties(fname='simhei.ttf', size=16)
# font2 = FontProperties(fname='Times New Roman.ttf', size=16)

plt.figure(figsize=(8, 6))
plt.yticks(fontproperties='Times New Roman', size=15)#设置大小及加粗
plt.xticks(fontproperties='Times New Roman', size=15)
plt.plot(10.0, 0.8, 'o-', label='omicron')
plt.plot(7.0, 1.3, 'o-', label='delta')
plt.plot(4.0, 1.2, 'o-', label='beta')
plt.plot(2.5, 6.6, 'o-', label='origin')
plt.plot(6.0, 25, 'o-', label='天花')
plt.plot(13, 0.2, 'o-', label='麻疹')
plt.plot(2.0, 2.5, 'o-', label='西班牙大流感')

plt.annotate('delta变异株', xy=(7.0, 2.0), xytext=(6.0, 6.0), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
             font=myfont)
plt.annotate('omicron变异株', xy=(10.0, 1.0), xytext=(9.0, 4.0), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
             font=myfont)
plt.annotate('原始新冠病毒', xy=(2.5, 7.0), xytext=(2.0, 10.0), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
             font=myfont)

plt.grid("True")
plt.legend(loc='upper right', prop=myfont, frameon=False)
plt.xlabel('基本再生数', font=myfont2)
plt.ylabel('死亡率（百分比）', font=myfont2)
# plt.savefig('{}_dailynew_confirmed_day{}.jpg'.format('香港', disp_days), dpi=200)
plt.show()
