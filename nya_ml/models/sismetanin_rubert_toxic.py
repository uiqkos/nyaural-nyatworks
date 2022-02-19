from nya_ml.models.bertclassifier import BertClassifier


class RuBertToxic(BertClassifier):
    _tokenizer = 'sismetanin/rubert-toxic-pikabu-2ch'
    _model = 'sismetanin/rubert-toxic-pikabu-2ch'
    _labels = ('no toxic', 'toxic')
    _label_grad = 0, 1
