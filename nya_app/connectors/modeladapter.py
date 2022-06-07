from nya_ml.models.model import Model
from nya_scraping.comment import Comment


class ModelAdapter(Model):
    @property
    def grad(self):
        return self.model.grad

    def __init__(self, model: Model):
        self.model = model

    def predict(self, comment: Comment):
        return self.model.predict(comment.text)

    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)
