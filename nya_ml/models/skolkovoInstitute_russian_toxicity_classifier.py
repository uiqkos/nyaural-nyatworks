from nya_ml.models.bertclassifier import BertClassifier


class RuToxicityClassifier(BertClassifier):
    _tokenizer = 'SkolkovoInstitute/russian_toxicity_classifier'
    _model = 'SkolkovoInstitute/russian_toxicity_classifier'
    _labels = ('no toxic', 'toxic')
    _label_grad = 0, 1
