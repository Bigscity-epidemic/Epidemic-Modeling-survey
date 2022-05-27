from utils import compare
import pandas as pd
import numpy as np

def euler():
    filename = "SEIR_euler.csv"
    dfmyresult = pd.DataFrame(pd.read_csv("./MyResult/" + filename))
    dfpaperresult = pd.DataFrame(pd.read_csv("PaperResult/" + filename))
    myResult = np.array(dfmyresult)[:,2]
    paperResult = np.array(dfpaperresult)[:,2]
    myResult /= 1000000.0
    paperResult /= 1000000.0
    length = myResult.shape[0]
    mae = compare.get_MAE(paperResult, myResult)
    mse = compare.get_MSE(paperResult, myResult)
    rmse = compare.get_RMSE(paperResult, myResult)
    mape = compare.get_MAPE(paperResult, myResult)
    print(mae,mse,rmse, mape)

def sde():
    my = np.zeros([101])
    paper = np.zeros([101])
    for i in range(100):
        filename = str(i+1)+".csv"
        dfmyresult = pd.DataFrame(pd.read_csv("./MyResult/SEIR_SDE/" + filename))
        dfpaperresult = pd.DataFrame(pd.read_csv("PaperResult/SEIR_SDE/" + filename,header = None))
        myResult = np.array(dfmyresult)[:, 2]
        paperResult = np.array(dfpaperresult)[:, 2]
        myResult /= 1000000.0
        paperResult /= 1000000.0
        my += myResult
        paper += paperResult

    mae = compare.get_MAE(paperResult, myResult)
    mse = compare.get_MSE(paperResult, myResult)
    rmse = compare.get_RMSE(paperResult, myResult)
    mape = compare.get_MAPE(paperResult, myResult)
    print(mae, mse, rmse, mape)
euler()
sde()