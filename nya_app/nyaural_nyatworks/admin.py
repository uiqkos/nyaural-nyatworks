# ####### DB models ####### #
from django.contrib import admin
from nya_app.nyaural_nyatworks.models import Report, Dataset, Train

admin.register(Report, Dataset, Train)

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
)(ConstRandModel)

model_registrar.register(
    name='const_random', target='toxic',
    save_to_db=True, db_name='Random constant'
)(ConstRandModel)

model_registrar.register(
    name='const_random', target='sarcasm',
    save_to_db=True, db_name='Random constant'
)(ConstRandModel)

# ####### RuBert sentiment by blanchefort ####### #
from nya_ml.models.blanchefort_rubert_sentiment import RuBertSentiment

model_registrar.register(
    name='blanchefort/rubert-sentiment', target='sentiment',
    save_to_db=True, db_name='RuBert by blanchefort'
)(RuBertSentiment)

# ####### RuBert toxic by sismetanin ####### #
from nya_ml.models.sismetanin_rubert_toxic import RuBertToxic

model_registrar.register(
    name='sismetanin/rubert-toxic', target='toxic',
    save_to_db=True, db_name='RuBert by sismetanin'
)(RuBertToxic)

# ####### RuBert toxic by SkolkovoInstitute ####### #
from nya_ml.models.skolkovoInstitute_russian_toxicity_classifier import RuToxicityClassifier

model_registrar.register(
    name='SkolkovoInstitute/russian_toxicity_classifier', target='toxic',
    save_to_db=True, db_name='Russian toxicity classifier by SkolkovoInstitute'
)(RuToxicityClassifier)
