import numpy as np
import ml.nn
import torch
import json

model = ml.nn.NeuralNetwork()
model.load_state_dict(torch.load('ml/model_weights.pth'))
model.eval()
with open('ml/transformed_data/vars.json', 'r') as infile:
    vars = json.load(infile)

class ModelEvaluator:
    def __init__(self):
        self.model = ml.nn.NeuralNetwork()
        self.model.load_state_dict(torch.load('ml/model_weights.pth'))
        self.model.eval()
        with open('ml/transformed_data/vars.json', 'r') as infile:
            self.vars = json.load(infile)

    def evaluate(self, input):
        input = (np.array(input) - self.vars["min"]) / (
                    self.vars["max"] - self.vars["min"])
        pred = self.model(torch.tensor(input.tolist())) * (vars["max"]-vars["min"]) + vars["min"]
        return round(pred.item(),1)