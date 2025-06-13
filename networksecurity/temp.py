import pandas as pd
import numpy as np

df = pd.read_csv("../Network_Data/phisingData.csv")

print("NA rows: ",df.isna().sum())