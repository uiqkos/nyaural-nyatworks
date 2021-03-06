from typing import Dict, Type

from nya_app.nyaural_nyatworks.models import Model as DBModel
from nya_ml.models.model import Model


class Registrar:
    def __init__(self):
        self._registered_models: Dict[str, Type[Model]] = {}
        self._cashed_models: Dict[str, Model] = {}

    def get_model(self, name) -> Model:
        if name in self._cashed_models:
            model = self._cashed_models[name]

        else:
            model = self._registered_models[name].load()
            self._cashed_models[name] = model

        return model

    def register(self, name: str, target: str, save_to_db: bool = False, db_name: str = None):
        local_name = target + '_' + name

        if save_to_db and not DBModel.objects.filter(local_name=local_name).exists():
            DBModel(
                local_name=local_name,
                name=db_name,
                target=target,
                struct={}
            ).save()

        def wrapper(model_type: Type[Model]) -> Type[Model]:
            self._registered_models[local_name] = model_type

            return model_type

        return wrapper
