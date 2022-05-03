from nya_ml.models.bertclassifier import BertClassifier


class TatyanaRuBertSentiment(BertClassifier):
    _tokenizer = "Tatyana/rubert-base-cased-sentiment-new"
    _model = "Tatyana/rubert-base-cased-sentiment-new"
    _grad = {
        'NEUTRAL': 1,
        'POSITIVE': 0,
        'NEGATIVE': 2
    }
