from utils import compare
import pandas as pd
import numpy as np


filename = "result.csv"
dfmyresult = pd.DataFrame(pd.read_csv("./MyResult/" + filename))
dfpaperresult = pd.DataFrame(pd.read_csv("PaperResult/" + filename))
myResult = np.array(dfmyresult)[:,3]
paperResult = np.array(dfpaperresult)[:,4]
myResult /= 45000000
paperResult /= 45000000
length = myResult.shape[0]
mae = compare.get_MAE(paperResult, myResult)
mse = compare.get_MSE(paperResult, myResult)
rmse = compare.get_RMSE(paperResult, myResult)
mape = compare.get_MAPE(paperResult, myResult)
print(mae,mse,rmse, mape)
