from nya_ml.models.bertclassifier import BertClassifier


class BlanchefortRuBertSentiment(BertClassifier):
    _tokenizer = 'blanchefort/rubert-base-cased-sentiment-rusentiment'
    _model = 'blanchefort/rubert-base-cased-sentiment-rusentiment'
    _grad = {
        'neutral': 1,
        'positive': 0,
        'negative': 2
    }
