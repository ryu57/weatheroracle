import torch
import pandas as pd
import numpy as np
import math
import pickle
import json
from torch.utils.data import Dataset

with open('transformed_data/file_name.txt', 'rb') as f:
    file_name = pickle.load(f)
data = pd.read_csv("raw_data/tor_island.csv")
actual_data = data["MEAN_TEMPERATURE"].tolist()
mx , mn = max(actual_data) , min(actual_data)

arr = []
i = 0
while i < len(actual_data) - 11:
    jump = 0
    for k in range(12):
        if math.isnan(actual_data[i+k]):
            jump = k + 1
    if jump > 0:
        i += jump
        continue
    else:
        temp = np.array(actual_data[i:i + 10])
        temp = (temp - mn) / (mx - mn)
        arr.append([temp.tolist(), (actual_data[i + 11] - mn) / (mx - mn)])
    i += 1

header = ['Past 10', 'Target']
df = pd.DataFrame(arr, columns=header)
print(df)
file_name += 1
df.to_pickle('transformed_data/{}.pkl'.format(file_name))
jsn = {"max": mx, "min": mn}

with open('transformed_data/vars.json', 'w') as f:
    json.dump(jsn, f)


with open('transformed_data/file_name.txt', 'wb') as f:
    pickle.dump(file_name,f)


