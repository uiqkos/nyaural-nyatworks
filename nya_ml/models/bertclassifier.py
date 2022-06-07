import gc
from abc import ABC
from operator import methodcaller

import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast

from nya_ml.models.model import Model


class BertClassifier(Model, ABC):
    _tokenizer = None
    _model = None
    _grad: dict = None

    def __init__(self, tokenizer, model, device):
        self.tokenizer = tokenizer
        self.model = model.to(device)
        self.device = device

    @property
    def grad(self):
        return self._grad

    def _predict(self, text):
        with torch.no_grad():
            inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')

            tokens_tensor = inputs['input_ids'].to(self.device)
            token_type_ids = inputs['token_type_ids'].to(self.device)
            attention_mask = inputs['attention_mask'].to(self.device)

            outputs = self.model(**{
                'input_ids' : tokens_tensor,
                'token_type_ids' : token_type_ids,
                'attention_mask' : attention_mask
            })

            predicted = torch.softmax(outputs.logits, dim=1)

        predicted = predicted.to('cpu')

        del inputs, tokens_tensor, token_type_ids, attention_mask, outputs
        gc.collect()

        return predicted

    @torch.no_grad()
    def predict(self, text):
        predicted = self._predict(text)
        predicted = list(map(lambda t: t.item(), predicted[0]))
        # predicted = predicted[0][self._labels - 1].item()
        return dict(zip(
            self._grad.keys(),
            predicted
        ))

    @classmethod
    def load(cls, device='cpu'):
        tokenizer = BertTokenizerFast.from_pretrained(cls._tokenizer)
        model = AutoModelForSequenceClassification.from_pretrained(cls._model, return_dict=True)

        return cls(tokenizer, model, device)
