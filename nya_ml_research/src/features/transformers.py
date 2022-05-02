import string
from abc import ABC
from collections import namedtuple
from collections.abc import Iterable
from copy import deepcopy
from functools import reduce
from itertools import filterfalse
from typing import Union

import pandas as pd
from commonregex import *
from fn import F
from nltk import SnowballStemmer, WordNetLemmatizer, corpus, LancasterStemmer, RegexpStemmer, PorterStemmer, \
    RegexpTokenizer
from sklearn.base import BaseEstimator, TransformerMixin
from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def compose2(f1, f2):
    return lambda *args, **kwargs: f2(f1(*args, **kwargs))


def compose(*funcs):
    return reduce(compose2, funcs)


def apply(func, X):
    if isinstance(X, pd.DataFrame):
        return X.applymap(func)
    if isinstance(X, pd.Series):
        return X.apply(func)
    if isinstance(X, Iterable):
        return list(map(func, X))

    return func(X)


class Serializable(ABC):
    # todo save to json
    pass


class Cleaner(BaseEstimator, TransformerMixin):
    def __init__(self,
                 ips=True,
                 emails=True,
                 links=True,
                 dates=True,
                 addresses=True,
                 punctuation=True):

        self.stages = {}

        def add_pattern_remover(name, pattern):
            self.stages[name] = F(re.sub, pattern, '')

        if emails:
            add_pattern_remover('email_remover', email)

        if ips:
            add_pattern_remover('ip_remover', ip)

        if dates:
            date_pattern = "([\d]{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s[\d]{4})"
            add_pattern_remover('simple_date_remover', re.compile(date_pattern, re.IGNORECASE))
            add_pattern_remover('date_remover', date)

        if links:
            add_pattern_remover('link_remover', link)

        if addresses:
            add_pattern_remover('street_address_remover', street_address)

        if punctuation:
            add_pattern_remover('punctuation_remover', f'[{string.punctuation}]')

        self.punctuation = punctuation
        self.emails = emails
        self.ips = ips
        self.dates = dates
        self.links = links
        self.addresses = addresses

        self.preprocessor = compose(
            *self.stages.values()
        )

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        return apply(self.preprocessor, X)


class Splitter(BaseEstimator, TransformerMixin):
    def __init__(self):  # todo _tokenize method
        self.tokenizer = RegexpTokenizer(r"[\w\*]+[`']?\w{0,2}")

    def fit(self, X, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        return apply(self.tokenizer.tokenize, X)


class Stemmer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stemmer = None

    def with_stemmer(self,
                     stemmer='snowball',
                     *args,
                     **kwargs):
        if not isinstance(stemmer, str):
            self.stemmer = stemmer

        elif stemmer == 'snowball':
            self.stemmer = SnowballStemmer(*args, **kwargs)

        elif stemmer == 'porter':
            self.stemmer = PorterStemmer(*args, **kwargs)

        elif stemmer == 'lancaster':
            self.stemmer = LancasterStemmer(*args, **kwargs)

        elif self.stemmer in ('_regex', 'regexp', 'r'):
            self.stemmer = RegexpStemmer(*args, **kwargs)

        else:
            raise Exception(f'Invalid value for stemmer: {stemmer}')

        return self

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        if self.stemmer is not None:
            return apply(F(map, self.stemmer.stem) >> list, X)
        return X


class Lemmatizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        return apply(F(map, self.lemmatizer.lemmatize) >> list, X)


class StopWordsRemover(BaseEstimator, TransformerMixin):
    def __init__(self, language='english'):
        self.language = language
        self.stopwords = corpus.stopwords.words(language)

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        return apply(F(filterfalse, self.stopwords.__contains__) >> list, X)


class Tokenizer(BaseEstimator, TransformerMixin):
    def __init__(self,
                 pad=False,
                 tokenizer=None,
                 pad_len: Union[type(None), int] = None):

        if tokenizer is None:
            tokenizer = KerasTokenizer()

        self.pad = pad
        self.pad_len = pad_len
        self.pad_len_method = 'max' if pad_len is None else 'const'

        self.tokenizer = tokenizer

    def fit(self, X, *args, **kwargs):
        self.tokenizer.fit_on_texts(X)

        if self.pad_len_method == 'max':
            current_max = max(map(len, X))

            if self.pad_len is None:
                self.pad_len = current_max
            else:
                self.pad_len = max(self.pad_len, current_max)

        return self

    def transform(self, X, *args, **kwargs):
        if self.pad:
            return pad_sequences(
                self.tokenizer.texts_to_sequences(X),
                maxlen=self.pad_len,
                *args,
                **kwargs
            )

        return self.tokenizer.texts_to_sequences(X)
