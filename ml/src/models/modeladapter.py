from typing import Type, Dict

from ml.src.models.registrar import registrar
from nyaural_nyatworks.models import Model as DBModel
from ml.src.comment import Comment
from ml.src.models.model import Model


class ModelAdapter(Model):
    _registered_models: Dict[str, Type[Model]] = {}
    _cashed_models: Dict[str, Type[Model]] = {}

    def __init__(self, db_model: DBModel):
        self.db_model = db_model
        self.model = registrar.get_model(db_model.local_name)

    def predict(self, comment: Comment):
        return self.model.predict(comment.text)
