import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class Net(nn.Module):
    """
    CNN model for lift classification with 3 output layers classifying 
    the lift as Squat, Bench, or Deadlift
    """

    def __init__(self):
        super().__init__()
        #define a 3 layer CNN
        self.conv1 = nn.Conv2d(3, 64, 5)
        self.conv2 = nn.Conv2d(64, 128, 5)
        self.maxpool_layer = nn.MaxPool2d(2, stride=2)
        self.fc_layer = nn.Linear(128 * 5 * 5, 120)
        self.fc_layer2 = nn.Linear(120, 84)
        self.fc_layer2 = nn.Linear(84, 3)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
