import numpy as np
from sklearn.metrics import mean_squared_error
cumuU=[  250,   308,   368,   414,   487,   548,   617,   735,   850,
        1021,  1180,  1389,  1658,  1940,  2310,  2750,  3297,  3909,
        4530,  5714,  6862,  8327, 10125, 12035, 13929, 15846, 17682,
       19583, 21134, 22874, 24427, 27566, 29187, 30717, 32119, 33631,
       34793, 35931, 37014, 37805, 38952, 39746, 40703, 41612, 42313,
       42860, 43366, 44020, 44597, 44931, 45219, 45606, 45865, 46086,
       46274, 46479, 46688, 46794, 46902, 46969]
du=np.diff(cumuU)
print(du)
df=np.load('Ucumm.npy')
pred=[]
for i in range(100):
    pred.append(0)
for area in range(len(df)):
    for j in range(len(df[area])):
        pred[j]+=df[area][j]
pred=pred[:len(du)+1]
dp=np.diff(np.array(pred))
print(dp)
r=np.mean(np.abs((dp-du)/du))*100
print(r)