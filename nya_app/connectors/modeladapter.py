from nya_app.connectors import Registrar
from nya_ml.models.model import Model
from nya_scraping.comment import Comment


class ModelAdapter(Model):
    def __init__(self, model: Model):
        self.model = model

    def predict(self, comment: Comment):
        return self.model.predict(comment.text)


class ModelAdapterFactory:
    def __init__(self, registrar: Registrar):
        self.registrar = registrar

    def create(self, db_model):
        return ModelAdapter(self.registrar.get_model(db_model.local_name))
