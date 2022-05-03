import torch
from torch import nn


class LogisticRegression(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()

        self.lin = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        x = x.float()
        x = self.lin(x)
        x = torch.sigmoid(x)

        return x
