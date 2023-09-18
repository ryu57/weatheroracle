import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import pandas as pd

class WeatherDataset(Dataset):
    def __init__(self, filename):
        self.data = pd.read_pickle(filename)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return torch.tensor(self.data['Past 7'][item]), self.data['Target'][item]


