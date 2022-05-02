# ####### DB models ####### #
from django.contrib import admin
from nya_app.nyaural_nyatworks.models import Report, Model

admin.register(Report, Model)

# ####### ML models ####### #
from nya_app.connectors.registrar import Registrar

model_registrar = Registrar()

# ####### ConstRandModel ####### #
from nya_ml.models.constmodel import ConstRandModel

model_registrar.register(
    name='const_random',
    target='sentiment',
    save_to_db=True,
    db_name='Random constant'
)(ConstRandModel('positive', ('positive', 'negative')))

model_registrar.register(
    name='const_random', target='toxic',
    save_to_db=True, db_name='Random constant'
)(ConstRandModel('toxic', ('toxic', 'no toxic')))

model_registrar.register(
    name='const_random', target='sarcasm',
    save_to_db=True, db_name='Random constant'
)(ConstRandModel('sarcasm', ('sarcasm', 'no sarcasm')))

# ####### RuBert sentiment by blanchefort ####### #
from nya_ml.models.blanchefort_rubert_sentiment import BlanchefortRuBertSentiment

model_registrar.register(
    name='blanchefort_rubert_sentiment', target='sentiment',
    save_to_db=True, db_name='RuBert by blanchefort'
)(BlanchefortRuBertSentiment)

# ####### RuBert sentiment by Tatyana ####### #
from nya_ml.models.tatyana_rubert_sentiment import TatyanaRuBertSentiment

model_registrar.register(
    name='tatyana_rubert_sentiment', target='sentiment',
    save_to_db=True, db_name='RuBert by Tatyana'
)(TatyanaRuBertSentiment)

# ####### RuBert toxic by sismetanin ####### #
from nya_ml.models.sismetanin_rubert_toxic import SismetaninRuBertToxic

model_registrar.register(
    name='sismetanin_rubert_toxic', target='toxic',
    save_to_db=True, db_name='RuBert by sismetanin'
)(SismetaninRuBertToxic)

# ####### RuBert toxic by SkolkovoInstitute ####### #
from nya_ml.models.skolkovoInstitute_russian_toxicity_classifier import SkolkovoRuToxicityClassifier

model_registrar.register(
    name='SkolkovoInstitute_russian_toxicity_classifier', target='toxic',
    save_to_db=True, db_name='Russian toxicity classifier by SkolkovoInstitute'
)(SkolkovoRuToxicityClassifier)
