import torch
import pandas as pd
import numpy as np
import math
import pickle
from torch.utils.data import Dataset

with open('transformed_data/file_name.txt', 'rb') as f:
    file_name = pickle.load(f)
data = pd.read_csv("raw_data/tor_island.csv")
actual_data = data["MEAN_TEMPERATURE"].tolist()

arr = []
i = 0
while i < len(actual_data) - 8:
    jump = 0
    for k in range(9):
        if math.isnan(actual_data[i+k]):
            jump = k + 1
    if jump > 0:
        i += jump
        continue
    else:
        arr.append([actual_data[i:i+7], actual_data[i + 8]])
    i += 1

header = ['Past 7', 'Target']
df = pd.DataFrame(arr, columns=header)

file_name += 1
df.to_pickle('transformed_data/{}.pkl'.format(file_name))


with open('transformed_data/file_name.txt', 'wb') as f:
    pickle.dump(file_name,f)


