# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   Bgru.py
@Author     :   zilongyuan
@datetime   :    2023/2/25
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

import torch
import numpy as np

class DiyBgru(torch.nn.Module):
    def __init__(self, input_dim, hidden_size, out_size, n_layers=1, batch_size=1):
        super(DiyBgru, self).__init__()

        self.batch_size = batch_size
        self.hidden_size = hidden_size
        self.out_size = out_size
        self.n_layers = n_layers

        self.gru = torch.nn.GRU(input_dim, hidden_size, n_layers, batch_first=True, bidirectional=True)

        self.fc1 = torch.nn.Linear(hidden_size*2, 300)
        self.fc2 = torch.nn.Linear(300, out_size)

    def forward(self, x):
        h0 = torch.zeros(self.n_layers*2, x.shape[0], self.hidden_size)
        # c0 = torch.zeros(self.n_layers*2, x.size(0), self.hidden_size)
        output, hidden = self.gru(x, h0)  # batch_size, seq_length, hidden_size*2
        output = self.fc1(output)
        output = self.fc2(output)
        output = output[:, -1, :]

        return output, hidden

    def init_hidden(self):
        hidden = torch.autograd.Variable(torch.zeros(2*self.n_layers, self.batch_size, self.hidden_size, device='cpu'))

np.random.seed(2023)

def generate_slice(maxlen, vector_dim):
    # slice = [torch.rand(vector_dim) for _ in range(maxlen)]  # torch generate data
    # slice = [np.random.random(vector_dim) for _ in range(maxlen)]  # numpy generate data
    # slice = np.array(slice)

    slice = np.random.random((50, 30))
    # if slice.sum(axis=1)[0] > slice.sum(axis=1)[-1]:
    if np.sum(slice[:, 0]) > np.sum(slice[:, -1]):
        # 假设切片第一维和大于最后一维则为正
        label = 1
    else:
        label = 0
    return slice, label

def generate_slicelists(slice_num, maxlen, vector_dim):
    slicelists, labels = [], []
    for _ in range(slice_num):
        slices, label = generate_slice(maxlen, vector_dim)
        slicelists.append(slices)
        labels.append(label)
    return torch.tensor(slicelists, dtype=torch.float), torch.tensor(labels, dtype=torch.long)

if __name__ == '__main__':
    X, y = generate_slicelists(100, 50, 30)
    model = DiyBgru(input_dim=30, hidden_size=20, out_size=2)
    epochs = 50
    learning_rate = 0.001

    optim = torch.optim.Adam(model.parameters(), lr=learning_rate)
    crossLoss = torch.nn.CrossEntropyLoss()

    batch_size = 5
    for epoch in range(epochs):
        for i in range(len(X)//batch_size):
            outputs = model(torch.tensor(X[i*batch_size: (i+1)*batch_size, :, :], dtype=torch.float))
            loss = crossLoss(outputs[0], y[i*batch_size:(i+1)*batch_size])  # target 必须是long （int型）且比predict维度少一维，其值代表类别索引 注意输出的类别数要和其值对应，如果其值大于输出类别数则会爆越界错误
            optim.zero_grad()
            loss.backward()
            optim.step()
        print("="*10+'\n{} epoch {:.4f} loss'.format(epoch, loss))
    torch.save(model.state_dict(), './bgru.pth')

    # load
    model2 = DiyBgru(input_dim=30, hidden_size=20, out_size=2)
    model2.load_state_dict(torch.load('./bgru.pth'))
    model2.eval()

    test_x = torch.rand(1, 10, 30, dtype=torch.float)
    test_y = 1 if sum(test_x[0, :, 0]) > sum(test_x[0, :, -1]) else 0

    predict, hidden = model2(test_x)
    if torch.argmax(predict) == test_y:
        print('True')
    else:
        print('False')