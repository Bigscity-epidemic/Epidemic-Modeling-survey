from utils import compare
import pandas as pd
import numpy as np

D_a_tuple = [(50, 1), (50, 2), (50, 4), (100, 2), (100, 4), (100, 8)]

for d,a in D_a_tuple:
    filename = "Dcrit_"+str(d)+"_a_"+str(a)+".csv"
    dfmyresult = pd.DataFrame(pd.read_csv("./MyResult/" + filename))
    dfpaperresult = pd.DataFrame(pd.read_csv("PaperResult/" + filename,header = None))
    myResult = np.array(dfmyresult)[:,1]
    paperResult = np.array(dfpaperresult)[:,1]
    myResult = myResult
    paperResult = paperResult
    length = myResult.shape[0]
    mae = compare.get_MAE(paperResult, myResult)
    mse = compare.get_MSE(paperResult, myResult)
    rmse = compare.get_RMSE(paperResult, myResult)
    mape = compare.get_MAPE(paperResult, myResult)
    print(mae,mse,rmse, mape)

