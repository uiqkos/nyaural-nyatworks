import re
import string
from itertools import filterfalse

from fn import F
from nltk import SnowballStemmer, WordNetLemmatizer, corpus, LancasterStemmer, RegexpStemmer, PorterStemmer, \
    RegexpTokenizer

from utils import compose
from sklearn.base import BaseEstimator, TransformerMixin
from commonregex import *


class Cleaner(BaseEstimator, TransformerMixin):
    def __init__(self,
                 generator=False,
                 punctuation=True,
                 ips=True,
                 emails=True,
                 links=True,
                 dates=True,
                 addresses=True,):

        self.generator = generator
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
        if self.generator:
            return map(self.preprocessor, X)
        return list(map(self.preprocessor, X))


class Tokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, generator=False):  # todo tokenize method
        self.generator = generator
        self.tokenizer = RegexpTokenizer(r"[\w\*]+[`']?\w{0,2}")

    def fit(self, X, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        if self.generator:
            return map(self.tokenizer.tokenize, X)
        return list(map(self.tokenizer.tokenize, X))


class Stemmer(BaseEstimator, TransformerMixin):
    def __init__(self,
                 generator=False,
                 stemmer='snowball',
                 language='english',
                 *args,
                 **kwargs):

        self.generator = generator

        if stemmer == 'snowball':
            self.stemmer = SnowballStemmer(language=language, *args, **kwargs)

        elif stemmer == 'porter':
            self.stemmer = PorterStemmer(*args, **kwargs)

        elif stemmer == 'lancaster':
            self.stemmer = LancasterStemmer(*args, **kwargs)

        elif self.stemmer in ('regex', 'regexp', 'r'):
            self.stemmer = RegexpStemmer(*args, **kwargs)

        else:
            raise Exception(f'Invalid value for stemmer: {stemmer}')

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        if self.generator:
            return map(F(map, self.stemmer.stem) >> list, X)
        return list(map(F(map, self.stemmer.stem) >> list, X))


class Lemmatizer(BaseEstimator, TransformerMixin):
    def __init__(self, generator=False,):
        self.generator = generator
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        if self.generator:
            return map(F(map, self.lemmatizer.lemmatize) >> list, X)
        return list(map(F(map, self.lemmatizer.lemmatize) >> list, X))


class StopWordsRemover(BaseEstimator, TransformerMixin):
    def __init__(self,
                 generator=False,
                 language='english',
                 *args,
                 **kwargs):
        self.generator = generator
        self.stopwords = corpus.stopwords.words(language, *args, **kwargs)

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, *args, **kwargs):
        if self.generator:
            return map(F(filterfalse, self.stopwords.__contains__) >> list, X)
        return list(map(F(filterfalse, self.stopwords.__contains__) >> list, X))

