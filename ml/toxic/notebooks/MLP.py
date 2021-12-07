#%%
from typing import Union, List

from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Optimizer
import tensorflow.keras.optimizers as optimizers
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.layers import InputLayer, Dense, Dropout, Embedding
from gensim.models import Word2Vec

import keras_tuner as kt
import numpy as np
import pandas as pd

#%% md
## Load data

#%%
X_train = np.recfromcsv('../data/prepared_train.csv')
print(X_train.shape)
Y_train = pd.read_csv('../data/train.csv', header=0, index_col=0)
print(Y_train.shape)
Y_train.drop('comment_text', inplace=True, axis=1)
X_test = np.fromfile('../data/prepared_test.csv')
#%%

#%%

def choice_dict(name, hp: kt.HyperParameters, **options):
    return options[hp.Choice(name, options.keys())]

def choice_list(name, hp: kt.HyperParameters, *options):
    return options[hp.Int(name + '_index', 0, len(options) - 1)]

#%%
input_shape = (None, X_train.shape[1])
output_shape = (1, 5)

#%%

#%%

def build_model(
        w2v: Word2Vec,
        hidden_layers: int,
        hidden_layers_units: List[int],
        use_bias: bool,
        dropout: float,
        optimizer: Union[str, Optimizer],

):
    model = Sequential()

    model.add(
        Embedding(
            input_dim=len(w2v.wv),
            output_dim=w2v.vector_size,
            weights=w2v.wv.vectors
        )
    )

    for layer_index in range(hidden_layers):
        model.add(
            Dense(
                units=hidden_layers_units[layer_index],
                activation='relu',
                use_bias=use_bias
            )
        )

        if dropout != 0:
            model.add(
                Dropout(dropout)
            )

    model.add(
        Dense(
            units=output_shape[1],
            activation='sigmoid'
        )
    )

    model.compile(
        optimizer=optimizer,
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model

def build_model_from_hp(hp: kt.HyperParameters):
    return build_model(
        w2v=choice_dict(
            name='w2v', hp=hp,
            light=Word2Vec.load('light_word2vec.model'),
            heavy=Word2Vec.load('heavy_word2vec.model')
        ),
        hidden_layers=hp.Int('hidden_layers', 2, 10),
        hidden_layers_units=choice_list(
            'hidden_layers_units', hp,
            np.linspace(100, 10, 9, dtype=np.dtype('int64')),
            np.linspace(1000, 50, 9, dtype=np.dtype('int64')),
            np.linspace(1000, 50, 9, dtype=np.dtype('int64')),
            np.linspace(2000, 100, 9, dtype=np.dtype('int64')),
        ),
        use_bias=hp.Boolean('use_bias'),
        dropout=hp.Choice('dropout', [0., 0.3, 0.5]),
        optimizer=hp.Choice('optimizer', ['sgd', 'adam']),
    )

#%%
