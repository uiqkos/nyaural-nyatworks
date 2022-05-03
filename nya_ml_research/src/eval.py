from dataclasses import dataclass

import torch


@dataclass
class Eval:
    model: torch.nn.Module

    def __call__(self, engine, batch):
        self.model.eval()

        with torch.no_grad():
            x, y = batch
            y = y.float()

            y_pred = self.model(x)
            return y_pred, y
