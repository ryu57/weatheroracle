import pandas as pd
import torch
import torch.nn as nn
import random
import math
from nn import NeuralNetwork

data = pd.read_csv("data/tor_island.csv")

actual_data = data["MEAN_TEMPERATURE"].tolist()

train_data = actual_data[0:1700]
valid_data = actual_data[1700:2222]

model = NeuralNetwork()

learning_rate = 1e-6
batch_size = 5
epochs = 10000



loss_fn = nn.MSELoss()

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

def train_loop(train_data, model, loss_fn, optimizer):
    for i in range(batch_size):
        Nan_detected = True
        while Nan_detected:
            Nan_detected = False
            start = random.randrange(0,1694)
            extracted_data = train_data[start:start + 5]

            for k in extracted_data:
                if math.isnan(k):
                    Nan_detected = True

            if math.isnan(train_data[start+6]):
                break

            if Nan_detected:
                break

            data = torch.tensor(train_data[start:start + 5])
            y = torch.tensor([train_data[start+6]])


            pred = model(data)
            loss = loss_fn(pred, y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            # print(f"Loss: {loss} Pred: {pred.item()} Actual: {y.item()}")

def test_loop(valid_data, model, loss_fn):
    model.eval()

    test_loss, error = 0, 0
    n = 0
    with torch.no_grad():
        for i in range(516):
            n += 1
            pred = model(torch.tensor(valid_data[i:i+5]))
            test_loss += loss_fn(pred, torch.tensor([valid_data[i+6]])).item()
            error += abs(pred.item() - valid_data[i+6])

    print(f"Average error: {error/n}")

for t in range(epochs):
    train_loop(train_data, model, loss_fn, optimizer)

test_loop(valid_data, model, loss_fn)