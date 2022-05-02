from abc import ABC

import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast

from nya_ml.models.model import Model


class BertClassifier(Model, ABC):
    _tokenizer = None
    _model = None
    _grad: dict = None

    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    @property
    def grad(self):
        return self._grad

    @torch.no_grad()
    def _predict(self, text):
        inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**inputs)
        predicted = torch.softmax(outputs.logits, dim=1)
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
    def load(cls):
        tokenizer = BertTokenizerFast.from_pretrained(cls._tokenizer)
        model = AutoModelForSequenceClassification.from_pretrained(cls._model, return_dict=True)

        return cls(tokenizer, model)
