from nya_ml.models.bertclassifier import BertClassifier


class SismetaninRuBertToxic(BertClassifier):
    _tokenizer = 'sismetanin/rubert-toxic-pikabu-2ch'
    _model = 'sismetanin/rubert-toxic-pikabu-2ch'
    _grad = {
        'no toxic': 0,
        'toxic': 2
    }
