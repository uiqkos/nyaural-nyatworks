from typing import Dict, Type

from nyaural_nyatworks.models import Model as DBModel
from ml.src.models.model import Model


class Registrar:
    def __init__(self):
        self._registered_models: Dict[str, Type[Model]] = {}
        self._cashed_models: Dict[str, Type[Model]] = {}

    def get_model(self, name) -> Model:
        if name in self._cashed_models:
            model = self._cashed_models[name]

        else:
            model = self._registered_models[name].load()
            self._cashed_models[name] = model

        return model

    def register(self, name: str, target: str, save_to_db: bool = False, db_name: str = None):
        local_name = target + '/' + name

        if save_to_db and not DBModel.objects.filter(local_name=local_name).exists():
            DBModel(
                local_name=local_name,
                name=db_name,
                target=target,
                struct={}
            ).save()

        def wrapper(model_cls: Type[Model]) -> Type[Model]:
            self._registered_models[local_name] = model_cls

            return model_cls

        return wrapper


registrar = Registrar()

from .skolkovoInstitute_russian_toxicity_classifier import RuToxicityClassifier
from .sismetanin_rubert_toxic import RuBertToxic
from .blanchefort_rubert_sentiment import RuBertSentiment
from .constmodel import ConstRandModel

