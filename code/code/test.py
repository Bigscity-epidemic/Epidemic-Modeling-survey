import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import datetime as dt

formatter = DateFormatter("%b %d")
months = mdates.MonthLocator()
days = mdates.DayLocator(bymonthday=(7, 22))
days1 = mdates.DayLocator(bymonthday=(7, 22))
dayss = mdates.DayLocator()

_, axes = plt.subplots(1, 1, figsize=(13, 5))
ax = plt.subplot(111)
plt.plot(t_range_subdt[1:], np.diff(cumuU)[:], 'ko', label = 'Observation')
plt.plot(t_range_subdt[1:], np.diff(result[:, 3] + result[:, 4])[:], '.-', color='orange', label = 'Simulation', linewidth = 2)
plt.fill_between(t_range_subdt[1:], np.diff(result_down[:, 3] + result_down[:, 4])[:], np.diff(result_up[:, 3] + result_up[:, 4])[:], color = 'wheat', alpha = 0.6)
# plt.vlines(t_range_subdt[k1], -200, np.max(np.diff(result_up[:, 3] + result_up[:, 4])[:]), linestyles='dotted', color = 'grey')
# plt.vlines(t_range_subdt[k2], -200, np.max(np.diff(result_up[:, 3] + result_up[:, 4])[:]), linestyles='dotted', color = 'grey')
# plt.title(u'U of {} (Start from {})'.format(streetname, alldates[0]))
plt.xlabel('Date', fontsize = 14)
plt.ylabel('No. of onset cases', fontsize = 14)
plt.xticks(size = 13)
plt.yticks(size = 13)
# plt.gcf().autofmt_xdate()
span_xticks = 5
x = t_range_subdt[:]
plt.xticks(np.array(x)[np.arange(0, len(x), span_xticks)])
ax.xaxis.set_major_formatter(formatter)
# plt.grid(axis = 'y')
plt.legend(loc = 'upper left', frameon=False, fontsize = 15)
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
plt.xlim(t_range_subdt[0], t_range_subdt[-1])
plt.ylim(0)
plt.savefig('./result/extended_fig_5.pdf', bbox_inches='tight')