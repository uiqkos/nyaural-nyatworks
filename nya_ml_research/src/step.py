from dataclasses import dataclass

import torch


@dataclass
class Step:
    model: torch.nn.Module
    criterion: torch.nn.modules.loss._Loss
    optimizer: torch.optim.Optimizer

    def __call__(self, engine, batch):
        self.model.train()
        self.optimizer.zero_grad()

        x, y = batch

        y_pred = self.model(x)
        loss = self.criterion(y_pred, y.float())

        loss.backward()
        self.optimizer.step()

        return loss.item()
