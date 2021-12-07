from .toxic_model import ToxicPrediction, ToxicModel
from .toxic_model import fields as toxic_fields
import tensorflow.keras as keras


def load_model():
    return ToxicModel()

def get_keras_embedding():
    keras.layers.Embedding
