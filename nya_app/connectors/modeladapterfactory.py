from nya_app.connectors.modeladapter import ModelAdapter
from nya_app.connectors.registrar import Registrar


class ModelAdapterFactory:
    def __init__(self, registrar: Registrar):
        self.registrar = registrar

    def create(self, db_model):
        return ModelAdapter(self.registrar.get_model(db_model.local_name))
