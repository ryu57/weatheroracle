import ui
import api
import ml.nn
import torch
import datetime

mainUI = ui.MainUI()
mainUI.update_forecast()

requests = api.Requests()
history = requests.list_history()
model = ml.nn.NeuralNetwork()
model.load_state_dict(torch.load('ml/model_weights.pth'))
model.eval()

print(model(torch.tensor(history)))


mainUI.show()