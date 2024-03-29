import pandas as pd
import torch
import torch.nn as nn
import random
import math
import dataset
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from nn import NeuralNetwork

data = dataset.WeatherDataset("transformed_data/14.pkl")

train_data, valid_data = random_split(data, [0.7, 0.3], torch.Generator().manual_seed(42))
print(train_data)

model = NeuralNetwork()

learning_rate = 1e-4
batch_size = 10
epochs = 500

loss_fn = nn.MSELoss()

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

def train_loop(train_data, model, loss_fn, optimizer):
    model.train()
    for batch, (X, Y) in enumerate(train_data):


        pred = model(X)
        loss = loss_fn(torch.flatten(pred).double(), Y.double())
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # if batch % 400 == 0:
        #     loss = loss.item()
    # print(f"loss: {loss:>7f} ")
    valid_loop(DataLoader(valid_data, batch_size=10, shuffle=True), model, loss_fn)

def test_loop(valid_data, model, loss_fn):
    model.eval()

    test_loss, error = 0, []
    n = 0
    with torch.no_grad():
        for X, Y in valid_data:
            n += 1
            pred = model(X)
            test_loss += loss_fn(pred.flatten(), Y).item()
            error.append(abs(pred.item() - Y.item()))

    return error

def valid_loop(valid_data, model, loss_fn):
    model.eval()

    test_loss, error = 0, 0
    n = 0
    with torch.no_grad():
        for X, Y in valid_data:
            n += 1
            pred = model(X)
            test_loss += loss_fn(pred.flatten(), Y).item()

    # print(f"Average loss: {test_loss / n}")

for t in range(epochs):
    train_loop(DataLoader(train_data, batch_size=batch_size, shuffle=True), model, loss_fn, optimizer)

error = test_loop(DataLoader(valid_data, batch_size=1, shuffle=True), model, loss_fn)

import numpy as np
print(np.mean(error))
print(np.std(error))
print(1.645 * np.std(error) / len(error)**0.5)
print(1.96 * np.std(error) / len(error)**0.5)
print(2.576 * np.std(error) / len(error)**0.5)
# torch.save(model.state_dict(), 'model_weights.pth')