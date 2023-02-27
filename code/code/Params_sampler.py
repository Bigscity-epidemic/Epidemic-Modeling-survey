import numpy as np
import pandas as pd
import pickle
import json
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime
import numpy as np
import pandas as pd
import datetime as dt
from pymc import *
from time import time

group = int(sys.argv[1])
st_idx = group * 20
ed_idx = (group+1) * 20
print('Estimating parameters for group {}'.format(group))

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def str_to_dt(datestr):
    return dt.datetime.strptime(datestr, '%Y/%m/%d').date()
def dt_to_str(datedt):
    return datedt.strftime('%Y/%m/%d')

def save_obj(obj, name ):
    with open('./objs/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./objs/' + name + '.pkl', 'rb') as f:
        return pickle.load(f, encoding='utf-8')

mod1trace = {}; mod2trace = {}; mod3trace = {}
mod1params = {}; mod2params = {}; mod3params = {}
mod1stats = {}; mod2stats = {}; mod3stats = {}
for group in range(5):
    subdata = load_obj('model_trace-{}'.format(group))
    for key in subdata['mod1'].keys():
        mod1trace[key] = subdata['mod1'][key]
        mod2trace[key] = subdata['mod2'][key]
        mod3trace[key] = subdata['mod3'][key]
        
    subdata = load_obj('model_params-{}'.format(group))
    for key in subdata['mod1'].keys():
        mod1params[key] = subdata['mod1'][key]
        mod2params[key] = subdata['mod2'][key]
        mod3params[key] = subdata['mod3'][key]
    
    subdata = load_obj('model_stats-{}'.format(group))
    for key in subdata['mod1'].keys():
        mod1stats[key] = subdata['mod1'][key]
        mod2stats[key] = subdata['mod2'][key]
        mod3stats[key] = subdata['mod3'][key]
print(len(mod1trace), len(mod2trace), len(mod3trace))

ID_net_work = load_obj('ID_net_wuhan_time_new_work')
ID_net_home = load_obj('ID_net_wuhan_time_new_home')
ID_net_midday = load_obj('ID_net_wuhan_time_new_midday')
ID_net_night = load_obj('ID_net_wuhan_time_new_night')
ID_homepop = load_obj('ID_homepop')

population = pd.read_csv('./data/subdistrict_population.csv')
population = np.array(population)

net_work = {}; net_home = {}; net_midday = {}; net_night = {}
str_homepop = {}
for i in range(len(population)):
    for j in range(len(population)):
        try:
            net_work[(i, j)] = ID_net_work[(i+1, j+1)]
            net_home[(i, j)] = ID_net_home[(i+1, j+1)] 
            net_midday[(i, j)] = ID_net_midday[(i+1, j+1)] 
            net_night[(i, j)] = ID_net_night[(i+1, j+1)] 
        except:
            net_work[(i, j)] = {0: 0.}
            net_home[(i, j)] = {0: 0.}
            net_midday[(i, j)] = {0: 0.}            
            net_night[(i, j)] = {0: 0.}      
for i in range(len(population)):
    str_homepop[i] = ID_homepop[i+1]

confirmrate = np.array([19.94736842, 20.        , 19.84615385, 19.53061224, 19.275     ,
       19.234375  , 18.61111111, 18.1484375 , 18.10169492, 17.54301075,
       17.05325444, 17.55607477, 17.28421053, 17.59531773, 16.68472906,
       17.03010753, 16.9965096 , 17.37730061, 16.50224215, 16.55235811,
       15.92692939, 15.69458763, 15.16122343, 14.46686303, 13.99558824,
       13.31704981, 12.65609007, 11.84826236, 11.15333734, 10.89662447,
        9.59337349, 10.14923619,  9.21408451,  8.51659626,  7.91490765,
        7.47246022,  7.46791862,  6.83015873,  6.19141631,  5.82229965,
        5.61341853,  4.75606936,  4.34396135,  4.21878225,  4.57387863,
        4.17326733,  3.40185185,  5.70699708,  3.2365416 ,  3.8038674 ,
        3.85483871,  4.69362745,  3.59622642,  3.38235294,  2.1314554 ,
        2.52036199,  1.99543379,  2.15044248,  2.57272727,  1.79411765,
        2.19277108,  2.55555556,  1.98630137,  1.6       ,  1.5       ,
        1.70588235,  1.69620253,  1.7       ,  1.28      ,  1.26666667,
        1.26666667,  1.26666667,  1.26666667,  1.26666667,  1.26666667,
        1.26666667,  1.26666667,  1.26666667,  1.26666667,  1.26666667])



N = [x for x in population[:, 2]]
initE = [ 6,  5, 16,  3, 13,  8,  4,  7,  1,  3,  8, 10,  1,  5, 10,  1, 11,
        7,  6,  6,  1,  3,  8,  5,  3,  1,  3,  4,  9,  5,  1,  1,  4,  3,
        2,  5,  4,  0,  2,  6,  2,  5,  4,  6,  3,  6,  0,  5,  3,  1,  1,
        5,  1,  2,  1,  0,  4,  0,  5,  3,  2,  2,  3,  3,  0,  4,  2,  1,
        2,  1,  2,  0,  1,  2,  1,  0,  0,  2,  2,  0,  1,  2,  1,  0,  2,
        0,  1,  0,  0,  0,  0,  1,  2,  0,  0,  1,  0,  2,  2,  0,  0,  1,
        0,  2,  0,  0,  0,  1,  1,  0,  0,  0,  0,  1,  0,  0,  1,  0,  0,
        0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  1,  0,  0,  1,  0,  0]
initP = [ 1,  3,  3,  7,  3, 14,  1,  4,  1,  0,  6,  1,  1,  3,  0,  2,  1,
        1,  0,  3,  1,  1,  1,  3,  1,  0,  2,  2,  2,  0,  0,  2,  0,  0,
        1,  2,  1,  0,  0,  0,  0,  2,  0,  2,  1,  1,  0,  1,  0,  2,  0,
        0,  2,  1,  0,  2,  0,  2,  0,  5,  0,  1,  1,  2,  0,  0,  2,  1,
        0,  1,  2,  0,  0,  1,  0,  0,  2,  0,  0,  0,  1,  0,  0,  0,  1,
        1,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,
        0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0]
initU = [ 1,  8, 22,  7,  5, 34,  8,  3,  5,  1,  3,  3,  0,  0,  4,  2,  5,
        7,  3,  5,  1,  3, 11,  0,  0,  3,  2,  1,  6,  0,  0,  4,  1,  2,
        1,  0,  3,  3,  1,  5,  2,  4,  0,  2,  0,  3,  2,  2,  0,  1,  2,
        0,  1,  4,  0,  2,  1,  3,  2,  2,  0,  2,  1,  6,  0,  4,  0,  1,
        3,  1,  0,  1,  1,  2,  1,  1,  1,  0,  1,  1,  2,  0,  0,  0,  1,
        0,  1,  1,  0,  0,  0,  1,  0,  0,  0,  0,  1,  0,  2,  1,  0,  0,
        1,  1,  1,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0]
initI = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0]

cumuU = [  250,   308,   368,   414,   487,   548,   617,   735,   850,
        1021,  1180,  1389,  1658,  1940,  2310,  2750,  3297,  3909,
        4530,  5714,  6862,  8327, 10125, 12035, 13929, 15846, 17682,
       19583, 21134, 22874, 24427, 27566, 29187, 30717, 32119, 33631,
       34793, 35931, 37014, 37805, 38952, 39746, 40703, 41612, 42313,
       42860, 43366, 44020, 44597, 44931, 45219, 45606, 45865, 46086,
       46274, 46479, 46688, 46794, 46902, 46969]


def merge_net(net1, net2):
    res = {}
    for k in net1.keys():
        if k not in net2.keys():
            res[k] = net1[k]
        else:
            res[k] = net1[k] + net2[k]
    return res

# merge subdistrict

divide = 99
street_pair = load_obj('model_street')
for i in range(divide, len(N), 1):
    min_id = street_pair[i] 
    
    if min_id >= 0:
        N[min_id] = N[min_id] + N[i]
        initE[min_id] = initE[min_id] + initE[i]
        initP[min_id] = initP[min_id] + initP[i]
        initU[min_id] = initU[min_id] + initU[i]
        initI[min_id] = initI[min_id] + initI[i]
        
        str_homepop[min_id] = str_homepop[min_id] + str_homepop[i]

        for k in range(0, divide):
            if min_id == k:
                continue
            net_work[(k, min_id)] = merge_net(net_work[(k, min_id)], net_work[(k, i)])
            net_home[(k, min_id)] = merge_net(net_home[(k, min_id)], net_home[(k, i)])
            net_midday[(k, min_id)] = merge_net(net_midday[(k, min_id)], net_midday[(k, i)])
            net_night[(k, min_id)] = merge_net(net_night[(k, min_id)], net_night[(k, i)])
            
            net_work[(min_id, k)] = merge_net(net_work[(min_id, k)], net_work[(i, k)])
            net_home[(min_id, k)] = merge_net(net_home[(min_id, k)], net_home[(i, k)])
            net_midday[(min_id, k)] = merge_net(net_midday[(min_id, k)], net_midday[(i, k)])
            net_night[(min_id, k)] = merge_net(net_night[(min_id, k)], net_night[(i, k)])

for item in street_pair.items():
    streeto1 = item[0]
    streetd1 = item[1]
    if streeto1 >= 0 and streetd1 >= 0:
        for streeto2 in range(divide, len(N), 1):
            if streeto1 == streeto2:
                continue
            streetd2 = street_pair[streeto2]
            if streetd1 == streetd2 or streetd2 < 0:
                continue
            else:
                net_work[(streetd1, streetd2)] = merge_net(net_work[(streetd1, streetd2)], net_work[(streeto1, streeto2)])
                net_home[(streetd1, streetd2)] = merge_net(net_home[(streetd1, streetd2)], net_home[(streeto1, streeto2)])
                net_midday[(streetd1, streetd2)] = merge_net(net_midday[(streetd1, streetd2)], net_midday[(streeto1, streeto2)])
                net_night[(streetd1, streetd2)] = merge_net(net_night[(streetd1, streetd2)], net_night[(streeto1, streeto2)])

streetNum = divide

def get_bmi(sid):
    odt_dt = np.load('./data/odt_o99d99h24d60.npy')
    odt_dt = odt_dt.sum(axis = (0, 1, 2))
    res = {i: odt_dt[i] for i in range(odt_dt.shape[0])}
    return res

bmi = {}
for i in range(0, divide):
    bmi[i] = get_bmi(i)

def sim_seui(INPUT, q0, alpha1a, alpha1b, alpha1c, alpha1d, beta1e, beta1q, sigma, Udata, Pdata, t_range, N, kt=0):
#     print(kt)
    T = len(t_range)
    l = streetNum
    S = np.zeros((l, T))
    E = np.zeros((l, T))
    P = np.zeros((l, T))
    U = np.zeros((l, T))
    I = np.zeros((l, T))
    S[:, 0] = INPUT[:, 0]
    E[:, 0] = INPUT[:, 1]
    P[:, 0] = INPUT[:, 2]
    U[:, 0] = INPUT[:, 3]
    I[:, 0] = INPUT[:, 4]
    beta1e = np.copy(beta1e)
    beta1e = beta1e - beta1q

    for j in range(1, T):
        Utrans_A = np.zeros(l); Utrans_B = np.zeros(l); Utrans_C = np.zeros(l)
        Ptrans_A = np.zeros(l); Ptrans_B = np.zeros(l); Ptrans_C = np.zeros(l)
        BMIj = np.zeros(l)
        for st in range(l):
            for k in range(l):
                if st != k:
                    pop_ratio = N[k] / str_homepop[k]
                    Utrans_A[st] += get_traff_arr(net_home[(k, st)], j - 1 + kt) * U[k, j - 1] * pop_ratio / N[k]
                    Utrans_B[st] += get_traff_arr(net_work[(k, st)], j - 1 + kt) * U[k, j - 1] * pop_ratio / N[k]
                    Utrans_C[st] += (get_traff_arr(net_midday[(k, st)], j - 1 + kt) + get_traff_arr(net_night[(k, st)], j - 1 + kt)) * U[k, j - 1] * pop_ratio / N[k]
                    
                    Ptrans_A[st] += get_traff_arr(net_home[(k, st)], j - 1 + kt) * P[k, j - 1] * pop_ratio / N[k]
                    Ptrans_B[st] += get_traff_arr(net_work[(k, st)], j - 1 + kt) * P[k, j - 1] * pop_ratio / N[k]
                    Ptrans_C[st] += (get_traff_arr(net_midday[(k, st)], j - 1 + kt) + get_traff_arr(net_night[(k, st)], j - 1 + kt)) * P[k, j - 1] * pop_ratio / N[k]
            BMIj[st] = get_traff_arr(bmi[st], j - 1 + kt) / N[st]
        S[:, j] = S[:, j - 1] - BMIj * alpha1a * S[:, j - 1] * Utrans_A / N - BMIj * alpha1b * S[:, j - 1] * Utrans_B / N \
                            - BMIj * alpha1c * S[:, j - 1] * Utrans_C / N - BMIj * alpha1d * S[:, j - 1] * U[:, j - 1] / N \
                            - q0 * BMIj * alpha1a * S[:, j - 1] * Ptrans_A / N - q0 * BMIj * alpha1b * S[:, j - 1] * Ptrans_B / N \
                            - q0 * BMIj * alpha1c * S[:, j - 1] * Ptrans_C / N - q0 * BMIj * alpha1d * S[:, j - 1] * P[:, j - 1] / N
        E[:, j] = E[:, j - 1] + BMIj * alpha1a * S[:, j - 1] * Utrans_A / N + BMIj * alpha1b * S[:, j - 1] * Utrans_B / N \
                            + BMIj * alpha1c * S[:, j - 1] * Utrans_C / N + BMIj * alpha1d * S[:, j - 1] * U[:, j - 1] / N \
                            + q0 * BMIj * alpha1a * S[:, j - 1] * Ptrans_A / N + q0 * BMIj * alpha1b * S[:, j - 1] * Ptrans_B / N \
                            + q0 * BMIj * alpha1c * S[:, j - 1] * Ptrans_C / N + q0 * BMIj * alpha1d * S[:, j - 1] * P[:, j - 1] / N - E[:, j - 1] / beta1e
        P[:, j] = P[:, j - 1] + E[:, j - 1] / beta1e - P[:, j - 1] / beta1q
        U[:, j] = U[:, j - 1] + P[:, j - 1] / beta1q - sigma[j - 1] * U[:, j - 1]
        I[:, j] = I[:, j - 1] + sigma[j - 1] * U[:, j - 1]

    return np.array([S, E, P, U, I]).T

def simulate_multi(Edata, Pdata, Udata, Idata, q01, q02, q03, alpha1s, alpha2s, alpha3s, beta1e, beta1q, beta2e, beta2q, beta3e, beta3q, sigma, N = N[:streetNum]):
    if np.min(alpha1s) < 0 or np.min(alpha2s) < 0:
        print('Warning ', alpha1s, alpha2s)
    l = Edata.shape[0]
    INPUT1 = np.zeros((l, 5))
    INPUT1[:, 0] = N[:l]
    INPUT1[:, 1] = initE[:l]
    INPUT1[:, 2] = initP[:l]
    INPUT1[:, 3] = initU[:l]
    INPUT1[:, 4] = initI[:l]

    t_range = np.arange(0.0, t, 1.0)
#     print(INPUT1, INPUT2)
    RES1 = sim_seui(INPUT1, q01, alpha1s[0], alpha1s[1], alpha1s[2], alpha1s[3], beta1e, beta1q, sigma[:k1], Udata[:,:k1], Pdata[:, :k1], t_range[:k1], N)
#     print('phase1', RES1.shape)
#     print('phase2')
    RES2 = sim_seui(RES1[-1, :, :], q02, alpha2s[0], alpha2s[1], alpha2s[2], alpha2s[3], beta2e, beta2q, sigma[k1-1:k2], Udata[:,k1-1:k2], Pdata[:, k1-1:k2], t_range[k1-1:k2], N, k1)
    
    RES3 = sim_seui(RES2[-1, :, :], q03, alpha3s[0], alpha3s[1], alpha3s[2], alpha3s[3], beta3e, beta3q, sigma[k2-1:], Udata[:,k2-1:], Pdata[:, k2-1:], t_range[k2-1:], N, k2)
#     print(RES1.shape, RES2.shape, RES3.shape)
    RES = np.concatenate((RES1[:-1, :], RES2[:-1, :], RES3), axis = 0)
    
    return RES

def get_traff_arr(traff, t):
    if t < 0:
        return traff[0]
    if len(traff) < 1:
        return 0.
    while t >= len(traff):
        t -= 7
    return traff[t]

def get_arr(arr, t):
    if t >= len(arr):
        return arr[-1]
    return arr[t]

def sim_seui_single(INPUT, q0, alpha1a, alpha1b, alpha1c, alpha1d, beta1e, beta1q, sigma, Udata, Pdata, t_range, N, streetid, kt=0):
    print(kt)
    T = len(t_range)
    l = streetNum
    S = np.zeros(T)
    E = np.zeros(T)
    P = np.zeros(T)
    U = np.zeros(T)
    I = np.zeros(T)
    S[0] = INPUT[0]
    E[0] = INPUT[1]
    P[0] = INPUT[2]
    U[0] = INPUT[3]
    I[0] = INPUT[4]
    beta1e = beta1e - beta1q

    for j in range(1, T):
        Utrans_A = 0; Utrans_B = 0; Utrans_C = 0
        Ptrans_A = 0; Ptrans_B = 0; Ptrans_C = 0
        BMIj = get_traff_arr(bmi[streetid], j - 1 + kt) / N[streetid]
        for k in range(l):
            if streetid != k:
                pop_ratio = N[k] / str_homepop[k]
                Utrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                Utrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                Utrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Udata[k, j - 1] * pop_ratio / N[k]
                
                Ptrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                Ptrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                Ptrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Pdata[k, j - 1] * pop_ratio / N[k]
        S[j] = S[j - 1] - BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] - BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                         - BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] - BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                         - q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] - q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                         - q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] - q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid]
        E[j] = E[j - 1] + BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] + BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                         + BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] + BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                         + q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] + q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                         + q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] + q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid] - E[j - 1] / beta1e
        P[j] = P[j - 1] + E[j - 1] / beta1e - P[j - 1] / beta1q
        U[j] = U[j - 1] + P[j - 1] / beta1q - sigma[j - 1] * U[j - 1]
        I[j] = I[j - 1] + sigma[j - 1] * U[j - 1]

    return np.array([S, E, P, U, I]).T

def simulate_first(streetid, Edata, Pdata, Udata, Idata, q0, alpha1s, beta1e, beta1q, sigma, N = N[:streetNum]):
   
    if min(alpha1s) < 0 :
        print('Warning ', alpha1s)
    l = Edata.shape[0]
    INPUT1 = np.zeros(5)
    INPUT1[0] = N[streetid]
    INPUT1[1] = initE[streetid]
    INPUT1[2] = initP[streetid]
    INPUT1[3] = initU[streetid]
    INPUT1[4] = initI[streetid]
    
    t_range = np.arange(0.0, t, 1.0)
#     print(INPUT1, INPUT2)
    RES1 = sim_seui_single(INPUT1, q0, alpha1s[0], alpha1s[1], alpha1s[2], alpha1s[3], beta1e, beta1q, sigma[:k1], Udata[:,:k1], Pdata[:, :k1], t_range[:k1], N, streetid)
    
    return RES1

def simulate_second(streetid, Edata, Pdata, Udata, Idata, q01, q02, alpha1s, alpha2s, beta1e, beta1q, beta2e, beta2q, sigma, N = N[:streetNum]):

    if min(alpha1s) < 0 or min(alpha2s) < 0:
        print('Warning ', alpha1s, alpha2s)
    l = Edata.shape[0]
    INPUT1 = np.zeros(5)
    INPUT1[0] = N[streetid]
    INPUT1[1] = initE[streetid]
    INPUT1[2] = initP[streetid]
    INPUT1[3] = initU[streetid]
    INPUT1[4] = initI[streetid]
    
    t_range = np.arange(0.0, t, 1.0)
#     print(INPUT1, INPUT2)
    RES1 = sim_seui_single(INPUT1, q01, alpha1s[0], alpha1s[1], alpha1s[2], alpha1s[3], beta1e, beta1q, sigma[:k1], Udata[:,:k1], Pdata[:, :k1], t_range[:k1], N, streetid)
    
    RES2 = sim_seui_single(RES1[-1, :], q02, alpha2s[0], alpha2s[1], alpha2s[2], alpha2s[3], beta2e, beta2q, sigma[k1-1:k2], Udata[:,k1-1:k2], Pdata[:, k1-1:k2], t_range[k1-1:k2], N, streetid, k1)
    
    return RES2

def simulate_third(streetid, Edata, Pdata, Udata, Idata, q01, q02, q03, alpha1s, alpha2s, alpha3s, beta1e, beta1q, beta2e, beta2q, beta3e, beta3q, sigma, N = N[:streetNum]):

    if min(alpha1s) < 0 or min(alpha2s) < 0:
        print('Warning ', alpha1s, alpha2s)
    l = Edata.shape[0]
    INPUT1 = np.zeros(5)
    INPUT1[0] = N[streetid]
    INPUT1[1] = initE[streetid]
    INPUT1[2] = initP[streetid]
    INPUT1[3] = initU[streetid]
    INPUT1[4] = initI[streetid]
    
    t_range = np.arange(0.0, t, 1.0)
#     print(INPUT1, INPUT2)
    RES1 = sim_seui_single(INPUT1, q01, alpha1s[0], alpha1s[1], alpha1s[2], alpha1s[3], beta1e, beta1q, sigma[:k1], Udata[:,:k1], Pdata[:, :k1], t_range[:k1], N, streetid)
    
    RES2 = sim_seui_single(RES1[-1, :], q02, alpha2s[0], alpha2s[1], alpha2s[2], alpha2s[3], beta2e, beta2q, sigma[k1-1:k2], Udata[:,k1-1:k2], Pdata[:, k1-1:k2], t_range[k1-1:k2], N, streetid, k1)
    
    RES3 = sim_seui_single(RES2[-1, :], q03, alpha3s[0], alpha3s[1], alpha3s[2], alpha3s[3], beta3e, beta3q, sigma[k2-1:], Udata[:,k2-1:], Pdata[:, k2-1:], t_range[k2-1:], N, streetid, k2)
    
    RES = np.concatenate((RES1[:-1, :], RES2[:-1, :], RES3))
    
    return RES

def SEIR_MODEL1(Ecumm, Pcumm, Ucumm, Icumm, init_S, init_E, init_P, init_U, init_I, beta1q, sigma, streetid, Udata, Pdata, N, kt=0):
    print(kt)
    T = Ecumm.shape[1]
    l = Ecumm.shape[0]
    Ecumm = Ecumm[streetid]; Ucumm = Ucumm[streetid]; Icumm = Icumm[streetid]
    case_data = np.concatenate([Ecumm, Ucumm, Icumm])
    print(Ecumm.shape, case_data.shape)
    q0 = Uniform('q0', 1e-2, 2.0, value = 0.25)
    
    alpha1a = Uniform('alpha1a', 2e-7, 10e-2, value = 5e-5)
    alpha1b = Uniform('alpha1b', 2e-7, 10e-2, value = 5e-5)
    alpha1c = Uniform('alpha1c', 2e-7, 10e-2, value = 5e-5)
    alpha1d = Uniform('alpha1d', 2e-7, 10e-2, value = 5e-5)
    beta1e = Weibull('beta1e', alpha = 3.032805, beta = 7.239863 )
    
    @deterministic
    def sim(q0 = q0, alpha1a = alpha1a, alpha1b = alpha1b, alpha1c = alpha1c, alpha1d = alpha1d, beta1e = beta1e):
        S = np.zeros(T)
        E = np.zeros(T)
        P = np.zeros(T)
        U = np.zeros(T)
        S[0] = init_S[streetid]#s0
        E[0] = init_E[streetid]#e0
        P[0] = init_P[streetid]#p0
        U[0] = init_U[streetid]#u0
        cumulative_cases = np.zeros(3*T)
        cumulative_cases[0] = Ecumm[0]
        cumulative_cases[T] = Ucumm[0]
        cumulative_cases[2*T] = Icumm[0]

        for j in range(1, T):
            Utrans_A = 0; Utrans_B = 0; Utrans_C = 0
            Ptrans_A = 0; Ptrans_B = 0; Ptrans_C = 0
            BMIj = get_traff_arr(bmi[streetid], j - 1 + kt) / N[streetid]
            for k in range(l):
                if streetid != k:
                    pop_ratio = N[k] / str_homepop[k]
                    Utrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                    Utrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                    Utrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Udata[k, j - 1] * pop_ratio / N[k]

                    Ptrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                    Ptrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                    Ptrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Pdata[k, j - 1] * pop_ratio / N[k]
            S[j] = S[j - 1] - BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] - BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                             - BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] - BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                             - q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] - q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                             - q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] - q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid]
            E[j] = E[j - 1] + BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] + BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                             + BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] + BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                             + q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] + q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                             + q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] + q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid] - E[j - 1] / (beta1e - beta1q)
            P[j] = P[j - 1] + E[j - 1] / (beta1e - beta1q) - P[j - 1] / beta1q
            U[j] = U[j - 1] + P[j - 1] / beta1q - sigma[j - 1] * U[j - 1]
            cumulative_cases[j] = E[j]#cumulative_cases[j - 1] + alpha1 * S[j - 1] * e1[j] * Utrans + alpha1 * S[j - 1] * e2[j] * U[j - 1]
            cumulative_cases[j + T] = U[j]#cumulative_cases[j + T - 1] + beta1 * E[j - 1]
            cumulative_cases[j + 2*T] = cumulative_cases[j + 2*T - 1] + sigma[j - 1] * U[j - 1]
            
        return cumulative_cases
    cases = Lambda('cases', lambda sim = sim : sim)
    A = Poisson('A', mu = cases, value = case_data, observed = True)
    return locals()

def SEIR_MODEL2(Ecumm, infect_data, init_S, init_E, init_P, init_U, init_I, beta1q, sigma, streetid, Udata, Pdata, N, kt=0):
    print(kt)
    T = infect_data.shape[1]
    l = infect_data.shape[0]
    Ecumm = Ecumm[streetid]
    infect_data = infect_data[streetid, :]
    case_data = np.concatenate([Ecumm, infect_data])
    print(case_data.shape)
    q0 = Uniform('q0', 1e-2, 2.0, value = 0.25)
    alpha1a = Uniform('alpha1a', 2e-6, 10e-2, value = 5e-2)
    alpha1b = Uniform('alpha1b', 2e-6, 10e-2, value = 5e-2)
    alpha1c = Uniform('alpha1c', 2e-6, 10e-2, value = 5e-2)
    alpha1d = Uniform('alpha1d', 2e-6, 10e-2, value = 5e-2)
    beta1e = Weibull('beta1e', alpha = 3.032805, beta = 7.239863 )

    @deterministic
    def sim(q0 = q0, alpha1a = alpha1a, alpha1b = alpha1b, alpha1c = alpha1c, alpha1d = alpha1d, beta1e = beta1e):
        S = np.zeros(T)
        E = np.zeros(T)
        P = np.zeros(T)
        U = np.zeros(T)
        S[0] = init_S#s0
        E[0] = init_E#e0
        P[0] = init_P#p0
        U[0] = init_U#u0
        cumulative_cases = np.zeros(2*T)
        cumulative_cases[0] = Ecumm[0]
        cumulative_cases[T] = infect_data[0]

        for j in range(1, T):
            Utrans_A = 0; Utrans_B = 0; Utrans_C = 0
            Ptrans_A = 0; Ptrans_B = 0; Ptrans_C = 0
            BMIj = get_traff_arr(bmi[streetid], j - 1 + kt) / N[streetid]
            for k in range(l):
                if streetid != k:
                    pop_ratio = N[k] / str_homepop[k]
                    Utrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                    Utrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                    Utrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Udata[k, j - 1] * pop_ratio / N[k]

                    Ptrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                    Ptrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                    Ptrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Pdata[k, j - 1] * pop_ratio / N[k]
            S[j] = S[j - 1] - BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] - BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                             - BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] - BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                             - q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] - q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                             - q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] - q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid]
            E[j] = E[j - 1] + BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] + BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                             + BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] + BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                             + q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] + q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                             + q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] + q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid] - E[j - 1] / (beta1e - beta1q)
            P[j] = P[j - 1] + E[j - 1] / (beta1e - beta1q) - P[j - 1] / beta1q
            U[j] = U[j - 1] + P[j - 1] / beta1q - sigma[j - 1] * U[j - 1]
            cumulative_cases[j] = E[j]
            cumulative_cases[j + T] = cumulative_cases[j + T - 1] + P[j - 1] / beta1q

        return cumulative_cases
    cases = Lambda('cases', lambda sim = sim : sim)
    A = Poisson('A', mu = cases, value = case_data, observed = True)
    return locals()

def SEIR_MODEL3(infect_data, init_S, init_E, init_P, init_U, init_I, beta1q, sigma, streetid, Udata, Pdata, N, kt=0):
    print(kt)
    T = infect_data.shape[1]
    l = infect_data.shape[0]
    infect_data = infect_data[streetid, :]
    case_data = infect_data
    print(infect_data.shape)
    q0 = Uniform('q0', 1e-2, 2.0, value = 0.25)
    alpha1a = Uniform('alpha1a', 1e-6, 1e-1, value = 1e-4)
    alpha1b = Uniform('alpha1b', 1e-6, 1e-1, value = 1e-4)
    alpha1c = Uniform('alpha1c', 1e-6, 1e-1, value = 1e-4)
    alpha1d = Uniform('alpha1d', 1e-6, 1e-1, value = 1e-4)
    beta1e = Weibull('beta1e', alpha = 3.032805, beta = 7.239863 )
    
    @deterministic
    def sim(q0 = q0, alpha1a = alpha1a, alpha1b = alpha1b, alpha1c = alpha1c, alpha1d = alpha1d, beta1e = beta1e):
        S = np.zeros(T)
        E = np.zeros(T)
        P = np.zeros(T)
        U = np.zeros(T)
        S[0] = init_S#s0
        E[0] = init_E#e0
        P[0] = init_P#p0
        U[0] = init_U#u0
        cumulative_cases = np.zeros(T)
        cumulative_cases[0] = infect_data[0]

        for j in range(1, T):
            Utrans_A = 0; Utrans_B = 0; Utrans_C = 0
            Ptrans_A = 0; Ptrans_B = 0; Ptrans_C = 0
            BMIj = get_traff_arr(bmi[streetid], j - 1 + kt) / N[streetid]
            for k in range(l):
                if streetid != k:
                    pop_ratio = N[k] / str_homepop[k]
                    Utrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                    Utrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Udata[k, j - 1] * pop_ratio / N[k]
                    Utrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Udata[k, j - 1] * pop_ratio / N[k]

                    Ptrans_A += get_traff_arr(net_home[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                    Ptrans_B += get_traff_arr(net_work[(k, streetid)], j - 1 + kt) * Pdata[k, j - 1] * pop_ratio / N[k]
                    Ptrans_C += (get_traff_arr(net_midday[(k, streetid)], j - 1 + kt) + get_traff_arr(net_night[(k, streetid)], j - 1 + kt)) * Pdata[k, j - 1] * pop_ratio / N[k]
            S[j] = S[j - 1] - BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] - BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                             - BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] - BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                             - q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] - q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                             - q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] - q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid]
            E[j] = E[j - 1] + BMIj * alpha1a * S[j - 1] * Utrans_A / N[streetid] + BMIj * alpha1b * S[j - 1] * Utrans_B / N[streetid]                             + BMIj * alpha1c * S[j - 1] * Utrans_C / N[streetid] + BMIj * alpha1d * S[j - 1] * U[j - 1] / N[streetid]                             + q0 * BMIj * alpha1a * S[j - 1] * Ptrans_A / N[streetid] + q0 * BMIj * alpha1b * S[j - 1] * Ptrans_B / N[streetid]                             + q0 * BMIj * alpha1c * S[j - 1] * Ptrans_C / N[streetid] + q0 * BMIj * alpha1d * S[j - 1] * P[j - 1] / N[streetid] - E[j - 1] / (beta1e - beta1q)
            P[j] = P[j - 1] + E[j - 1] / (beta1e - beta1q) - P[j - 1] / beta1q
            U[j] = U[j - 1] + P[j - 1] / beta1q - sigma[j - 1] * U[j - 1]
            cumulative_cases[j] = cumulative_cases[j - 1] + P[j - 1] / beta1q

        return cumulative_cases
    cases = Lambda('cases', lambda sim = sim : sim)
    A = Poisson('A', mu = cases, value = case_data, observed = True)
    return locals()

allcumm = load_obj('allcumm')

sigma = np.divide(1, confirmrate)
Ecumm = Etrue = np.copy(allcumm['Ecumm'])
Pcumm = Ptrue = np.copy(allcumm['Pcumm'])
Ucumm = Utrue = np.copy(allcumm['Ucumm'])
Icumm = Itrue = np.copy(allcumm['Icumm'])
k1 = 23
k2 = 34
beta1q = 2.3
t = 80

mod1params = {}; mod2params = {}; mod3params = {}
mod1stats = {}; mod2stats = {}; mod3stats = {}
mod1trace = {}; mod2trace = {}; mod3trace = {}

print('running ', group, st_idx, ed_idx)
for streetid in range(streetNum)[st_idx:ed_idx]:
    print(streetid)
    streetname = streetid
    # print(N[streetid], initE[streetid], initU[streetid], initI[streetid], streetid, streetname)
    np.random.seed(202017)
    mod1 = SEIR_MODEL1(Ecumm[:streetNum, :k1], Pcumm[:streetNum, :k1], Ucumm[:streetNum, :k1], Icumm[:streetNum, :k1], N[:streetNum], initE[:streetNum], initP[:streetNum],
                       initU[:streetNum], initI[:streetNum], beta1q,
                       sigma[:k1], streetid, Utrue[:streetNum, :k1], Ptrue[:streetNum, :k1], N[:streetNum])
    mc = MCMC(mod1)
    mc.use_step_method(AdaptiveMetropolis, [mod1['alpha1a'], mod1['alpha1b'], mod1['alpha1c'], mod1['alpha1d'], mod1['beta1e'], mod1['q0']])#, mod1['s0'], mod1['e0']
    mc.sample(iter = 11000, burn = 1000, thin = 50, verbose = 0)

    alpha1s = [mod1['alpha1a'].stats()['mean'], mod1['alpha1b'].stats()['mean'], mod1['alpha1c'].stats()['mean'], mod1['alpha1d'].stats()['mean']]

    RES1 = simulate_first(streetid, Etrue[:streetNum, :], Ptrue[:streetNum, :], Utrue[:streetNum, :], Itrue[:streetNum, :], 
                            mod1['q0'].stats()['mean'], alpha1s, 
                            mod1['beta1e'].stats()['mean'], beta1q, sigma,
                            )
    print(np.sum(RES1[-1, 3]), np.sum(Ucumm[streetid, k1-1]))

    np.random.seed(202018)
    mod2 = SEIR_MODEL2(Ecumm[:streetNum, k1-1:k2], Ucumm[:streetNum, k1-1:k2]+Icumm[:streetNum, k1-1:k2], RES1[-1, 0],
                      RES1[-1, 1], RES1[-1, 2], RES1[-1, 3], RES1[-1, 4], beta1q,
                      sigma[k1-1:k2], streetid, Utrue[:streetNum, k1-1:k2], Ptrue[:streetNum, k1-1:k2], N[:streetNum], k1)
    mc = MCMC(mod2)
    mc.use_step_method(AdaptiveMetropolis, [mod2['alpha1a'], mod2['alpha1b'], mod2['alpha1c'], mod2['alpha1d'], mod2['beta1e'], mod2['q0']])#, mod2['s0'], mod2['e0']
    mc.sample(iter = 11000, burn = 1000, thin = 50, verbose = 0)

    alpha1s = [mod1['alpha1a'].stats()['mean'], mod1['alpha1b'].stats()['mean'], mod1['alpha1c'].stats()['mean'], mod1['alpha1d'].stats()['mean']]
    alpha2s = [mod2['alpha1a'].stats()['mean'], mod2['alpha1b'].stats()['mean'], mod2['alpha1c'].stats()['mean'], mod2['alpha1d'].stats()['mean']]

    RES2 = simulate_second(streetid, Etrue[:streetNum, :], Ptrue[:streetNum, :], Utrue[:streetNum, :], Itrue[:streetNum, :], 
                            mod1['q0'].stats()['mean'], mod2['q0'].stats()['mean'], alpha1s, alpha2s,
                            mod1['beta1e'].stats()['mean'], beta1q, mod2['beta1e'].stats()['mean'], beta1q, sigma,
                            )
    print(np.sum(RES2[-1, 3]), np.sum(Ucumm[streetid, k2-1]))

    np.random.seed(202018)
    mod3 = SEIR_MODEL3(Ucumm[:streetNum, k2-1:]+Icumm[:streetNum, k2-1:], RES2[-1, 0],
                      RES2[-1, 1], RES2[-1, 2], RES2[-1, 3], RES2[-1, 4], beta1q,
                      sigma[k2-1:], streetid, Utrue[:streetNum, k2-1:], Ptrue[:streetNum, k2-1:], N[:streetNum], k2)
    mc = MCMC(mod3)
    mc.use_step_method(AdaptiveMetropolis, [mod3['alpha1a'], mod3['alpha1b'], mod3['alpha1c'], mod3['alpha1d'], mod3['beta1e'], mod3['q0']])#, mod2['s0'], mod2['e0']
    mc.sample(iter = 11000, burn = 1000, thin = 50, verbose = 0)
    
    mod1params[streetid] = [mod1['alpha1a'].stats()['mean'], mod1['alpha1b'].stats()['mean'], mod1['alpha1c'].stats()['mean'], mod1['alpha1d'].stats()['mean'], mod1['beta1e'].stats()['mean'], mod1['q0'].stats()['mean']]
    mod2params[streetid] = [mod2['alpha1a'].stats()['mean'], mod2['alpha1b'].stats()['mean'], mod2['alpha1c'].stats()['mean'], mod2['alpha1d'].stats()['mean'], mod2['beta1e'].stats()['mean'], mod2['q0'].stats()['mean']]
    mod3params[streetid] = [mod3['alpha1a'].stats()['mean'], mod3['alpha1b'].stats()['mean'], mod3['alpha1c'].stats()['mean'], mod3['alpha1d'].stats()['mean'], mod3['beta1e'].stats()['mean'], mod3['q0'].stats()['mean']]
    
    mod1stats[streetid] = [mod1['alpha1a'].stats(), mod1['alpha1b'].stats(), mod1['alpha1c'].stats(), mod1['alpha1d'].stats(), mod1['beta1e'].stats(), mod1['q0'].stats()]
    mod2stats[streetid] = [mod2['alpha1a'].stats(), mod2['alpha1b'].stats(), mod2['alpha1c'].stats(), mod2['alpha1d'].stats(), mod2['beta1e'].stats(), mod2['q0'].stats()]
    mod3stats[streetid] = [mod3['alpha1a'].stats(), mod3['alpha1b'].stats(), mod3['alpha1c'].stats(), mod3['alpha1d'].stats(), mod3['beta1e'].stats(), mod3['q0'].stats()]
    
    mod1trace[streetid] = [mod1['alpha1a'].trace(), mod1['alpha1b'].trace(), mod1['alpha1c'].trace(), mod1['alpha1d'].trace(), mod1['beta1e'].trace(), mod1['q0'].trace()]
    mod2trace[streetid] = [mod2['alpha1a'].trace(), mod2['alpha1b'].trace(), mod2['alpha1c'].trace(), mod2['alpha1d'].trace(), mod2['beta1e'].trace(), mod2['q0'].trace()]
    mod3trace[streetid] = [mod3['alpha1a'].trace(), mod3['alpha1b'].trace(), mod3['alpha1c'].trace(), mod3['alpha1d'].trace(), mod3['beta1e'].trace(), mod3['q0'].trace()]
    
    alpha1s = [mod1['alpha1a'].stats()['mean'], mod1['alpha1b'].stats()['mean'], mod1['alpha1c'].stats()['mean'], mod1['alpha1d'].stats()['mean']]
    alpha2s = [mod2['alpha1a'].stats()['mean'], mod2['alpha1b'].stats()['mean'], mod2['alpha1c'].stats()['mean'], mod2['alpha1d'].stats()['mean']]
    alpha3s = [mod3['alpha1a'].stats()['mean'], mod3['alpha1b'].stats()['mean'], mod3['alpha1c'].stats()['mean'], mod3['alpha1d'].stats()['mean']]
    
    

res = {}
res['mod1'] = mod1params
res['mod2'] = mod2params
res['mod3'] = mod3params
save_obj(res, 'model_params_test-{}'.format(group))

res = {}
res['mod1'] = mod1stats
res['mod2'] = mod2stats
res['mod3'] = mod3stats
save_obj(res, 'model_stats_test-{}'.format(group))

res = {}
res['mod1'] = mod1trace
res['mod2'] = mod2trace
res['mod3'] = mod3trace
save_obj(res, 'model_trace_test-{}'.format(group))

print('Finish!')
