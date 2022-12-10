import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        #define a 3 layer CNN
        self.conv1 = nn.Conv2d(1, 32, 3, 1, 1) # 1 input channel, 32 output channels, 3x3 kernel, stride 1, padding 1
        self.conv2 = nn.Conv2d(32, 64, 3, 1, 1) # 32 input channels, 64 output channels, 3x3 kernel, stride 1, padding 1
        self.maxpool_layer = nn.MaxPool2d(2, 2) # 2x2 kernel, stride 2
        self.fc_layer = nn.Linear(64*5*5, 3) # 64*5*5 input features, 3 output features (for 3 classes)


    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.maxpool_layer(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.maxpool_layer(x)
        x = x.view(-1, 128*5*5) 
        x = torch.sigmoid(self.fc_layer(x))
        return x
        

    def train(self, trainloader, epochs, learning_rate):
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.parameters(), lr=learning_rate, momentum=0.9)
        for epoch in range(epochs):
            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                inputs, labels = data
                optimizer.zero_grad()
                outputs = self(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                if i % 200 == 199:
                    print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 200))
                    running_loss = 0.0
        print('Finished Training')