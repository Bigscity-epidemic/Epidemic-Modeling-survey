import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams["font.family"] = "Times New Roman"

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


sigma = np.divide(1, confirmrate)
k1 = 23
k2 = 34
Etrue = Ptrue = Utrue = Itrue = np.zeros((161, 60))
streetid = 0
streetname = 'Wuhan'
beta1qs = np.array([2.3, ] * streetNum)
t = 60
based_time = str_to_dt('2020/1/1')
t_range_subdt = [based_time + dt.timedelta(days = x) for x in range(t)]


def simulate_CI(mod1trace, mod2trace, mod3trace, simulate_multi_func, times = 100, seed = 202009, sigma = sigma):
    single_res = []
    np.random.seed(seed)
    for t in range(times):
        if t % 10 == 0:
            print('step {:d}'.format(t))
        alpha1s = [np.array([np.random.choice(mod1trace[i][j]) for i in range(streetNum)]) for j in range(4)]
        beta1es = np.array([np.random.choice(mod1trace[i][4]) for i in range(streetNum)])
        q01s = np.array([mod1params[i][5] for i in range(streetNum)])
        if mod2trace is None:
            alpha2s = alpha1s
            alpha3s = alpha1s
            beta2es = beta1es
            beta3es = beta1es
            q02s = q01s
            q03s = q02s
        elif mod3trace is None:
            alpha2s = [np.array([np.random.choice(mod2trace[i][j]) for i in range(streetNum)]) for j in range(4)]
            alpha3s = alpha2s
            beta2es = np.array([np.random.choice(mod2trace[i][4]) for i in range(streetNum)])
            beta3es = beta2es
            q02s = np.array([mod2params[i][5] for i in range(streetNum)])
            q03s = q02s
        else:
            alpha2s = [np.array([np.random.choice(mod2trace[i][j]) for i in range(streetNum)]) for j in range(4)]
            alpha3s = [np.array([np.random.choice(mod3trace[i][j]) for i in range(streetNum)]) for j in range(4)]
            beta2es = np.array([np.random.choice(mod2trace[i][4]) for i in range(streetNum)])
            beta3es = np.array([np.random.choice(mod3trace[i][4]) for i in range(streetNum)])
            q02s = np.array([mod2params[i][5] for i in range(streetNum)])
            q03s = np.array([mod3params[i][5] for i in range(streetNum)])
        result = simulate_multi_func(Etrue[:streetNum, :], Ptrue[:streetNum, :], Utrue[:streetNum, :], Itrue[:streetNum, :], 
                        q01s, q02s, q03s, alpha1s, alpha2s, alpha3s,
                        beta1es, beta1qs, beta2es, beta1qs, beta3es, beta1qs, sigma,
                        )
        result = np.sum(result, axis = 1)
        single_res.append(result)
    res_median = np.zeros(single_res[0].shape)
    res_up = np.zeros(single_res[0].shape)
    res_down = np.zeros(single_res[0].shape)
    res_mean = np.zeros(single_res[0].shape)
    for i in range(single_res[0].shape[0]):
        for j in range(single_res[0].shape[1]):
            vals = np.array([single_res[k][i][j] for k in range(len(single_res))])
            res_median[i][j] = np.percentile(vals, 50)
            res_up[i][j] = np.percentile(vals, 97.5)
            res_down[i][j] = np.percentile(vals, 2.5)
            res_mean[i][j] = np.mean([res_up[i][j], res_down[i][j]])
    return res_median, res_up, res_down, res_mean, single_res

# main simulation

result, result_up, result_down, result_mean, all_res = simulate_CI(mod1trace, mod2trace, mod3trace, simulate_multi)

# street_params[streetname] = (mod1['alpha1'].stats(), mod1['beta1'].stats(), mod2['alpha1'].stats(), mod2['beta1'].stats())

# Extended Data Fig. 5 (aggregated plot)

from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
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
ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
# plt.grid(axis = 'y')
plt.legend(loc = 'upper left', frameon=False, fontsize = 15)
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
plt.xlim(t_range_subdt[0], t_range_subdt[-1])
plt.ylim(0)
plt.savefig('./result/extended_fig_5.pdf', bbox_inches='tight')
# plt.show()

_tx = np.diff(cumuU)[:]
_x = np.concatenate([_tx[:30], _tx[31:]])
_ty = np.diff(result[:, 3] + result[:, 4])[:]
_y = np.concatenate([_ty[:30], _ty[31:]])

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.diff(y_true), np.diff(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true))
print("MAPE = {}".format(mean_absolute_percentage_error(_x, _y)))

# Simulate the infections by different transmission

def sim_seui2(INPUT, q0, alpha1a, alpha1b, alpha1c, alpha1d, beta1e, beta1q, sigma, Udata, Pdata, t_range, N, kt=0):
#     print(kt)
    T = len(t_range)
    l = streetNum
    S = np.zeros((l, T))
    E = np.zeros((l, T))
    P = np.zeros((l, T))
    U = np.zeros((l, T))
    I = np.zeros((l, T))
    P1 = np.zeros((l, T))
    P2 = np.zeros((l, T))
    P3 = np.zeros((l, T))
    P4 = np.zeros((l, T))
    S[:, 0] = INPUT[:, 0]
    E[:, 0] = INPUT[:, 1]
    P[:, 0] = INPUT[:, 2]
    U[:, 0] = INPUT[:, 3]
    I[:, 0] = INPUT[:, 4]
    P1[:, 0] = INPUT[:, 5]
    P2[:, 0] = INPUT[:, 6]
    P3[:, 0] = INPUT[:, 7]
    P4[:, 0] = INPUT[:, 8]
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
        P1[:, j] = P1[:, j - 1] + BMIj * alpha1a * S[:, j - 1] * Utrans_A / N + q0 * BMIj * alpha1a * S[:, j - 1] * Ptrans_A / N
        P2[:, j] = P2[:, j - 1] + BMIj * alpha1b * S[:, j - 1] * Utrans_B / N + q0 * BMIj * alpha1b * S[:, j - 1] * Ptrans_B / N
        P3[:, j] = P3[:, j - 1] + BMIj * alpha1c * S[:, j - 1] * Utrans_C / N + q0 * BMIj * alpha1c * S[:, j - 1] * Ptrans_C / N
        P4[:, j] = P4[:, j - 1] + BMIj * alpha1d * S[:, j - 1] * U[:, j - 1] / N + q0 * BMIj * alpha1d * S[:, j - 1] * P[:, j - 1] / N

    return np.array([S, E, P, U, I, P1, P2, P3, P4]).T

def simulate_multi2(Edata, Pdata, Udata, Idata, q01, q02, q03, alpha1s, alpha2s, alpha3s, beta1e, beta1q, beta2e, beta2q, beta3e, beta3q, sigma, N = N[:streetNum]):

    if np.min(alpha1s) < 0 or np.min(alpha2s) < 0:
        print('Warning ', alpha1s, alpha2s)
    l = Edata.shape[0]
    INPUT1 = np.zeros((l, 9))
    INPUT1[:, 0] = N[:l]
    INPUT1[:, 1] = initE[:l]
    INPUT1[:, 2] = initP[:l]
    INPUT1[:, 3] = initU[:l]
    INPUT1[:, 4] = initI[:l]

    t_range = np.arange(0.0, t, 1.0)
#     print(INPUT1, INPUT2)
    RES1 = sim_seui2(INPUT1, q01, alpha1s[0], alpha1s[1], alpha1s[2], alpha1s[3], beta1e, beta1q, sigma[:k1], Udata[:,:k1], Pdata[:, :k1], t_range[:k1], N)
#     print('phase1', RES1.shape)
#     print('phase2')
    RES2 = sim_seui2(RES1[-1, :, :], q02, alpha2s[0], alpha2s[1], alpha2s[2], alpha2s[3], beta2e, beta2q, sigma[k1-1:k2], Udata[:,k1-1:k2], Pdata[:, k1-1:k2], t_range[k1-1:k2], N, k1)
    
    RES3 = sim_seui2(RES2[-1, :, :], q03, alpha3s[0], alpha3s[1], alpha3s[2], alpha3s[3], beta3e, beta3q, sigma[k2-1:], Udata[:,k2-1:], Pdata[:, k2-1:], t_range[k2-1:], N, k2)
#     print(RES1.shape, RES2.shape, RES3.shape)
    RES = np.concatenate((RES1[:-1, :], RES2[:-1, :], RES3), axis = 0)
    
    return RES

result, result_up, result_down, result_mean, all_res = simulate_CI(mod1trace, mod2trace, mod3trace, simulate_multi2)

# Fig 2a

_, axes = plt.subplots(1, 1, figsize=(8, 5))
ax = plt.subplot(111)
plt.bar(t_range_subdt[:], (result[:, 5] + result[:, 6] + result[:, 7])[:], color = 'teal', label = 'Inter-subdistrict transmission')
plt.bar(t_range_subdt[:], (result[:, 8])[:], bottom = (result[:, 5] + result[:, 6] + result[:, 7])[:], color = 'mediumpurple', label = 'Intra-subdistrict transmission')
# plt.title(u'U of {} (Start from {})'.format(streetname, alldates[0]))
plt.xlabel('Date', size = 16)
plt.ylabel('No. of cumulative exposed cases', size = 16)
# plt.gcf().autofmt_xdate()
span_xticks = 7
x = t_range_subdt[:]
plt.xticks(np.array(x)[np.arange(0, len(x), span_xticks)])
ax.xaxis.set_major_formatter(formatter)
ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# plt.grid(axis = 'y')
plt.legend(frameon=False, fontsize = 17)
plt.xticks(size = 15)
plt.yticks(size = 15)
plt.xlim(t_range_subdt[0], t_range_subdt[-1])
plt.ylim(0, 50000)
plt.savefig('./result/figure_2a.pdf', bbox_inches='tight')
# plt.show()

# Fig 2b

# street_params[streetname] = (mod1['alpha1'].stats(), mod1['beta1'].stats(), mod2['alpha1'].stats(), mod2['beta1'].stats())
_, axes = plt.subplots(1, 1, figsize=(8, 5))
ax = plt.subplot(111)
plt.bar(t_range_subdt[:], (result[:, 7])[:], color = 'lightcoral', label = 'Off-peak')
plt.bar(t_range_subdt[:], (result[:, 5])[:], bottom = (result[:, 7])[:], label = 'Evening-peak')
plt.bar(t_range_subdt[:], (result[:, 6])[:], bottom = (result[:, 7] + result[:, 5])[:], color = 'orange', label = 'Morning-peak')
# plt.title(u'U of {} (Start from {})'.format(streetname, alldates[0]))
plt.xlabel('Date', size = 16)
plt.ylabel('No. of cumulative exposed cases', size = 16)
# plt.gcf().autofmt_xdate()
span_xticks = 7
x = t_range_subdt[:]
plt.xticks(np.array(x)[np.arange(0, len(x), span_xticks)])
ax.xaxis.set_major_formatter(formatter)
ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# plt.grid(axis = 'y')
plt.legend(frameon=False, fontsize = 15)
plt.xticks(size = 15)
plt.yticks(size = 15)
plt.xlim(t_range_subdt[0], t_range_subdt[-1])
plt.ylim(0, 3000)
plt.savefig('./result/figure_2b.pdf', bbox_inches='tight')
# plt.show()

inoutflow = pd.DataFrame(data = {
    '0-Date': t_range_subdt,
    '1-Evening-peak': result[:, 5],
    '1-Morning-peak': result[:, 6],
    '1-Off-peak': result[:, 7],
    '1-Intra-subdistrict': result[:, 8],
    '2-Evening-peak-CIup': result_up[:, 5],
    '2-Morning-peak-CIup': result_up[:, 6],
    '2-Off-peak-CIup': result_up[:, 7],
    '2-Intra-subdistrict-CIup': result_up[:, 8],
    '3-Evening-peak-CIdown': result_down[:, 5],
    '3-Morning-peak-CIdown': result_down[:, 6],
    '3-Off-peak-CIdown': result_down[:, 7],
    '3-Intra-subdistrict-CIdown': result_down[:, 8],
})
inoutflow.to_excel('./result/figure_2ab_data.xlsx', index=False)

# print('Random-Evening-Morning')
# print(result[:, 7][22] / (result[:, 7] + result[:, 5]+ result[:, 6])[22], result[:, 5][22] /(result[:, 7] + result[:, 5]+ result[:, 6])[22], result[:, 6][22] / (result[:, 7] + result[:, 5]+ result[:, 6])[22])
# print(result_up[:, 7][22] / (result_up[:, 7] + result_up[:, 5]+ result_up[:, 6])[22], result_up[:, 5][22] /(result_up[:, 7] + result_up[:, 5]+ result_up[:, 6])[22], result_up[:, 6][22] / (result_up[:, 7] + result_up[:, 5]+ result_up[:, 6])[22])
# print(result_down[:, 7][22] / (result_down[:, 7] + result_down[:, 5]+ result_down[:, 6])[22], result_down[:, 5][22] /(result_down[:, 7] + result_down[:, 5]+ result_down[:, 6])[22], result_down[:, 6][22] / (result_down[:, 7] + result_down[:, 5]+ result_down[:, 6])[22])

print('Finish!')