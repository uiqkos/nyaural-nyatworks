from nya_ml.models.bertclassifier import BertClassifier


class RuBertSentiment(BertClassifier):
    _tokenizer = 'blanchefort/rubert-base-cased-sentiment-rusentiment'
    _model = 'blanchefort/rubert-base-cased-sentiment-rusentiment'
    _labels = ('neutral', 'positive', 'negative')
    _label_grad = 1, 0, 2
