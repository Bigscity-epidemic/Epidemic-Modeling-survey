from utils import compare
import pandas as pd
import numpy as np

TRUE = np.array(pd.read_csv("./PaperResult/SizeWinterI.csv"))
PRED = np.array(pd.read_csv("./MyResult/SizeWinterI.csv"))


TRUE = TRUE.flatten()
PRED = PRED.flatten()

print(TRUE.shape)
print(PRED.shape)