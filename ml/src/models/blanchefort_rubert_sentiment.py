import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast

from ml.src.model import Model


class RuBertSentiment(Model):
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    @torch.no_grad()
    def predict(self, comment):
        text = comment.text
        inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**inputs)
        predicted = torch.softmax(outputs.logits, dim=1)
        # predicted = predicted[0][2].item()
        # predicted = torch.argmax(predicted, dim=1).numpy()
        return str(predicted)

    @classmethod
    def load(cls):
        tokenizer = BertTokenizerFast.from_pretrained(
            'blanchefort/rubert-base-cased-sentiment')
        model = AutoModelForSequenceClassification.from_pretrained(
            'blanchefort/rubert-base-cased-sentiment', return_dict=True)

        return cls(tokenizer, model)
