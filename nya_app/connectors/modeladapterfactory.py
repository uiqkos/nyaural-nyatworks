import importlib
from functools import cache
from typing import Type

from nya_app.connectors.modeladapter import ModelAdapter
from nya_app.nyaural_nyatworks.models import Model as DBModel
from nya_ml.models.model import Model as MLModel


class ModelAdapterFactory:
    def import_cls(self, db_model: DBModel) -> Type[MLModel]:
        package = importlib.import_module(db_model.local_path)
        cls = getattr(package, db_model.class_name)
        return cls

    @cache
    def create(self, db_model: DBModel):
        return ModelAdapter(self.import_cls(db_model).load())
