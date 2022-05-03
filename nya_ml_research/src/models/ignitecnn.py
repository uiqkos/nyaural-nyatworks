from typing import List

import torch
import torch.nn.functional as F
from torch import nn


class TextCNN(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int,
        kernel_sizes: List[int],
        num_filters: int,
        num_classes: int,
        d_prob: float,
        embedding_weights: torch.Tensor
    ):
        super(TextCNN, self).__init__()

        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.kernel_sizes = kernel_sizes
        self.num_filters = num_filters
        self.num_classes = num_classes
        self.d_prob = d_prob

        self.embedding = nn.Embedding(vocab_size, embedding_dim, _weight=embedding_weights)
        self.embedding.requires_grad_(False)

        self.conv = nn.ModuleList([
            nn.Conv1d(
                in_channels=embedding_dim,
                out_channels=num_filters,
                kernel_size=k,
                stride=1
            ) for k in kernel_sizes
        ])

        self.dropout = nn.Dropout(d_prob)

        self.fc = nn.Linear(len(kernel_sizes) * num_filters, num_classes)

    def forward(self, x):
        x = self.embedding(x).transpose(1, 2)
        # print(x.size())

        x = [F.relu(conv(x)) for conv in self.conv]
        # print([x_.size() for x_ in x])
        x = [F.max_pool1d(c, c.size(-1)).squeeze(dim=-1) for c in x]
        # print([x_.size() for x_ in x])

        x = torch.cat(x, dim=1)
        # print(x.size())
        x = self.fc(self.dropout(x))
        # print(x.size())

        return torch.sigmoid(x).squeeze()

