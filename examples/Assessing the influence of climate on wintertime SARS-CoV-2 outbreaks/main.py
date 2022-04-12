import numpy as np
import pandas as pd
from SIRS import *
from datetime import datetime
#read file
NYcases = pd.read_csv("NYcases.csv", encoding='utf8')
NYq = pd.read_csv("NYq.csv", encoding='utf8')
NYestimR = pd.read_csv("NYestimR.csv", encoding='utf8')


#init value
IList = np.flip(np.arange(0.005, 0.5, 0.01))

RChangeVar = np.arange(0.65, 1, 0.01)

SOut = np.repeat(np.nan, len(IList))

SizeClimWinterI = np.full((len(IList), len(RChangeVar)), np.nan)
SizeWinterI = np.full((len(IList), len(RChangeVar)), np.nan)
TimingClimWinterI = np.full((len(IList), len(RChangeVar)), np.nan)
TimingWinterI = np.full((len(IList), len(RChangeVar)), np.nan)

#统计数据中日期的第一天是当年的第几天
startcases = datetime.strptime(NYestimR['date'][0], "%Y-%m-%d").timetuple().tm_yday
firstDayInDate = startcases
lead_time = firstDayInDate
end_data_time = max([datetime.strptime(d, "%Y-%m-%d") for d in NYestimR['date']]).timetuple().tm_yday

casesI = np.concatenate((np.repeat(0,startcases-1), np.diff(NYcases['cases'])),axis=0)

popuse = 8000000

for j in range(len(RChangeVar)):
    SOut = np.repeat(np.nan, len(IList))

    for i in range(len(IList)):
        # run the model with climate driven R0
        ISetStart = IList[i]
        RChangeUse = RChangeVar[j]

        predNPI = runModel(lead_time, NYestimR['Median(R)'], ISet=ISetStart,SSet='Orig', Rchange=RChangeUse)

        ratio = np.mean(predNPI['I'][:len(casesI)])/np.mean(casesI)
        casesI = casesI * ratio

        minSClim = min(predNPI['S'][1:end_data_time]) / popuse
        SOut[i] = minSClim

        ts = np.arange(1,10,1/364)[1:len(predNPI['I'])]
        I = predNPI['I']
        WinterI = [t for t in ts if t > 1.75 and t < 2.25 ]
        maxWinterIClim = max(WinterI)/popuse
        SizeClimWinterI[i,j] = maxWinterIClim
        I[0:end_data_time-1] = 0
        index = np.where(I == np.max(I[:708]))[0]
        if len(index) > 0: index = index[0]
        timeMax = ts[index]
        TimingClimWinterI[i,j] = timeMax

        # run the model under constant scenario
        R0equivclim = predNPI['I'][lead_time + NYestimR.shape[0]]
        R0listNew = np.concatenate((NYestimR['Median(R)'], np.repeat(R0equivclim,2000)), axis=0)[:2000]

        predConstant = runModel(lead_time, R0listNew, ISet=ISetStart,SSet='Orig',)

        ts = np.arange(1, 10, 1 / 364)[1:len(predNPI['I'])]
        I = predConstant['I']
        WinterI = [t for t in ts if t > 1.75 and t < 2.25]
        maxWinterIConst = max(WinterI) / popuse
        SizeWinterI[i, j] = maxWinterIConst
        I[0:end_data_time - 1] = 0
        index = np.where(I == np.max(I[:708]))[0]
        if len(index) > 0: index = index[0]
        timeMax = ts[index]
        TimingWinterI[i, j] = timeMax

np.savetxt("./Result/SizeClimWinterI.csv", SizeClimWinterI, delimiter=",")
np.savetxt("./Result/SizeWinterI.csv", SizeWinterI, delimiter=",")
np.savetxt("./Result/TimingClimWinterI.csv", TimingClimWinterI, delimiter=",")
np.savetxt("./Result/TimingWinterI.csv", TimingWinterI, delimiter=",")



