from nya_ml.models.bertclassifier import BertClassifier


class SkolkovoRuToxicityClassifier(BertClassifier):
    _tokenizer = 'SkolkovoInstitute/russian_toxicity_classifier'
    _model = 'SkolkovoInstitute/russian_toxicity_classifier'
    _grad = {
        'no toxic': 0,
        'toxic': 2
    }
