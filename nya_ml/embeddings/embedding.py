import gensim
import numpy as np
import torch
from torchtext.vocab import vocab


class Embedding:
    def __init__(self, model: gensim.models.KeyedVectors):
        self.model = model

    def get_torch_tensor_embeddings(self, insert_unk=True) -> torch.Tensor:
        if insert_unk:
            return torch.from_numpy(np.concatenate((
                np.zeros((1, self.model.vectors.shape[1])),
                self.model.vectors
            )))
        return torch.from_numpy(self.model.vectors)

    def to_gensim(self) -> gensim.models.KeyedVectors:
        return self.model

    def get_vocab(self, insert_unk=True):
        v = vocab(self.model.key_to_index, min_freq=0)  # mb specials

        if insert_unk:
            v.insert_token('<unk>', 0)
            v.set_default_index(v['<unk>'])

        return v
