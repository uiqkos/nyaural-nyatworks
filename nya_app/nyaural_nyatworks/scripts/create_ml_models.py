from nya_app.nyaural_nyatworks.scripts.load_env import *

from nya_app.nyaural_nyatworks.models import Model as DBModel

if __name__ == '__main__':
    DBModel(
        local_name='sentiment_const_random',
        local_path='nya_ml.models.constmodel',
        class_name='sentiment',
        target='sentiment',
        name='Random constant',
        struct={}
    ).save()

    DBModel(
        local_name='toxic_const_random',
        local_path='nya_ml.models.constmodel',
        class_name='toxic',
        target='toxic',
        name='Random constant',
        struct={}
    ).save()

    DBModel(
        local_name='sarcasm_const_random',
        local_path='nya_ml.models.constmodel',
        class_name='sarcasm',
        target='sarcasm',
        name='Random constant',
        struct={}
    ).save()

    DBModel(
        local_name='blanchefort_rubert_sentiment',
        local_path='nya_ml.models.blanchefort_rubert_sentiment',
        class_name='BlanchefortRuBertSentiment',
        target='sentiment',
        name='RuBert by blanchefort',
        struct={}
    ).save()

    DBModel(
        local_name='tatyana_rubert_sentiment',
        local_path='nya_ml.models.tatyana_rubert_sentiment',
        class_name='TatyanaRuBertSentiment',
        target='sentiment',
        name='RuBert by Tatyana',
        struct={}
    ).save()

    DBModel(
        local_name='sismetanin_rubert_toxic',
        local_path='nya_ml.models.sismetanin_rubert_toxic',
        class_name='SismetaninRuBertToxic',
        target='toxic',
        name='RuBert by sismetanin',
        struct={}
    ).save()

    DBModel(
        local_name='SkolkovoInstitute_russian_toxicity_classifier',
        local_path='nya_ml.models.skolkovoInstitute_russian_toxicity_classifier',
        class_name='SkolkovoRuToxicityClassifier',
        target='toxic',
        name='Russian toxicity classifier by SkolkovoInstitute',
        struct={}
    ).save()
