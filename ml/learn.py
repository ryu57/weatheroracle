import pandas as pd
import torch
import torch.nn as nn
import random
import math
import dataset
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from nn import NeuralNetwork

data = dataset.WeatherDataset("transformed_data/5.pkl")

train_data, valid_data = random_split(data, [0.7, 0.3], torch.Generator().manual_seed(42))


model = NeuralNetwork()

learning_rate = 1e-6
batch_size = 7
epochs = 10

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

        if batch % 5 == 0:
            loss = loss.item()
            print(f"loss: {loss:>7f} ")

def test_loop(valid_data, model, loss_fn):
    model.eval()

    test_loss, error = 0, 0
    n = 0
    with torch.no_grad():
        for X, Y in valid_data:
            n += 1
            pred = model(X)
            test_loss += loss_fn(pred.flatten(), Y).item()
            error += abs(pred.item() - Y)

    print(f"Average error: {error.item() / n}")

for t in range(epochs):
    train_loop(DataLoader(train_data, batch_size=batch_size, shuffle=True), model, loss_fn, optimizer)

test_loop(DataLoader(valid_data, batch_size=1, shuffle=True), model, loss_fn)

torch.save(model.state_dict(), 'model_weights.pth')