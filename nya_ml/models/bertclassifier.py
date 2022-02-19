from abc import ABC

import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast

from nya_ml.models.model import Model


class BertClassifier(Model, ABC):
    _tokenizer = None
    _model = None
    _labels = ()
    _label_grad = ()

    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    @torch.no_grad()
    def predict(self, text):
        inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**inputs)
        predicted = torch.softmax(outputs.logits, dim=1)
        predicted = list(map(lambda t: t.item(), predicted[0]))
        # predicted = predicted[0][self._labels - 1].item()
        return dict(zip(
            map(self._labels.__getitem__, self._label_grad),
            map(predicted.__getitem__, self._label_grad)
        ))

    @classmethod
    def load(cls):
        tokenizer = BertTokenizerFast.from_pretrained(cls._tokenizer)
        model = AutoModelForSequenceClassification.from_pretrained(cls._model, return_dict=True)

        return cls(tokenizer, model)
