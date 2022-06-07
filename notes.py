# я не шиз

# # import pathlib
# #
# # import spacy as spacy
# #
# # Any = type('Any', (), {})
# #
# # train = Any()
# # toxic_models = Any()
# # DATA_PATH = pathlib.Path(__file__)
# #
# #
# # train(
# #     model=toxic_models.get('LargeCNN.v2', preprocessor='FullPipeline.v3'),
# #     data=DATA_PATH.joinpath('processed', 'kaggle-toxic-comments-processed')
# # )
# #
# # cfg = {
# #     'data': [
# #         {
# #             'name': 'toxic-comments',
# #             'link': 'https://www.toxic-comments.com'
# #         }
# #     ],
# #
# #     'models': [
# #         {
# #             name
# #         }
# #     ]
# # }
# #
# #
# # get(
# #     'localhost/api/predict/',
# #     tree=[
# #         {
# #             'author': '...',
# #             'text': '...',
# #             'tree': [
# #                 ...
# #             ]
# #         }
# #     ],
# #     models=[
# #         {
# #             'name': 'LargeCNN.v2',
# #             'target': 'toxic',
# #             'preprocessor': {
# #                 'name': 'ru.default',
# #             }
# #         },
# #         {
# #             'target': 'sentiment',
# #             'name': 'SmallLSTM.v2',
# #             'preprocessor': 'spacy.default'
# #         }
# #     ],
# # )
# #
# # def load_model(model):
# #     with open(MODELS_PATH.joinpath(model['target'], model['name'] + '-' + model['preprocessor']['name'])) as f:
# #         m = models.get(model['name']).load_weights(f)
# #         return m
# #
# #
# # def predict(tree, models):
# #     data = parse(tree)
# #     models = [load_model(model) for model in models]
# #     predictions = {}
# #
# #     for model in models:
# #         predictions[model.target].append(model.predict(data))
# #
# #     return {
# #         'toxic': [
# #             0.1, 0.8324, 0.01, 0.0
# #         ],
# #         'sentiment': [
# #             0.1, 0.3324, 0.9999, 0.0
# #         ]
# #     }
# from dataclasses import dataclass, fields, asdict
# from operator import attrgetter
#
# from dataclasses_json import dataclass_json
#
#
# @dataclass
# class Data:
#     data_field: str
#
#     @property
#     def fields(self):
#         return fields(self)
#
# @dataclass
# class Data1(Data):
#     data1_field: str
#
# @dataclass
# class Data2(Data):
#     data2_field: str
#
# @dataclass
# class Decorator:
#     def __init__(self, data):
#         self._data = data
#         self._fields = fields(self._data)
#
#     def __getattr__(self, item):
#         if item in list(map(attrgetter('name'), self._fields)):
#             return self._data.__dict__[item]
#         return self.__dict__[item]
#
#     @property
#     def fields(self):
#         return fields(self._data)
#
# @dataclass
# class Decorator1(Decorator, Data):
#     decored_field1: str
#
#     def __init__(self, decored_field1, data):
#         self
#         self.decored_field1 = decored_field1
#
#
# if __name__ == '__main__':
#     d1 = Data1('1', '1')
#     d2 = Data2('2', '2')
#
#     dd1 = Decorator1('a', d1)
#     dd2 = Decorator1('a', d2)
#
#     print(asdict(dd1))
#     print(asdict(dd2))

# if __name__ == '__main__':
#     c_ = Comment(
#         '1', comments=[
#             Comment('1.1'),
#             Comment(
#                 '1.2',
#                 comments=[
#                     Comment(
#                         '1.2.1',
#                         comments=[
#                             Comment('1.2.1.1'),
#                             Comment('1.2.1.2'),
#                             Comment('1.2.1.3'),
#                         ]
#                     )
#                 ]
#             ),
#             Comment('1.3')]
#     )

# print(dir(LabeledComment(c_)))

# c_ = iterate_comment_level(c_)
# for c in map(LabeledComment, c_):
#     print(json.dumps(c.to_dict(comments=False), indent=4))

# c_ = map_comment(LabeledComment, c_)
# print(json.dumps(c_.to_dict(), indent=4))
#
# c_ = map_comment(StyledComment, c_)
# print(json.dumps(c_.to_dict(comments=False), indent=4))
#
# for c in iterate_comment_level(c_):
#     print(c.to_dict())

# lc = LabeledComment.from_comment(c_, sentiment={'positive': 100})
# print(json.dumps(lc.to_dict(), indent=4))

# mapper = partial(LabeledComment.from_comment, predictors={'toxic': NoneFactory}, sentiment={'positive': 100})
#
# lc = map_comment(c_, mapper)
#
# print(json.dumps(lc.to_dict(), indent=4))
# print(lc.to_dict())
# from nya_app.connectors.comments import CommentOneDim
# from nya_scraping.comment import Comment
#
# if __name__ == '__main__':
#     c = Comment('', id='hello')
#     c = CommentOneDim(c)
#     print(c.id)
#
# def AMetaMeta(**meta_kwargs):
#     class AMeta(type):
#         def __new__(cls, name, bases, dct, **kwargs):
#             return type(name, bases, {**dct, **meta_kwargs})
#     return AMeta
#
#
# class A(metaclass=AMetaMeta(a='a_keka')):
#     def __init__(self, a):
#         self.a = a
#
#
# class Base:
#     b = None
#
#
# def BBase(**kwargs) -> Base:
#     return type('base', (), kwargs)
#
#
# class B(BBase(b=3)):
#     def __init__(self, b):
#         self.b = b
#
#
# class RuWikiCorpora_300_10:
#     @classmethod
#     def load(cls):
#         pass


# static_value = 'static_value'


# Factory
# class BBaseFactory:
#     def __init__(self, **kwargs):
#         self.kwargs = kwargs
#
#     def create(self):
#         return type('BBase', (), self.kwargs)
#
#
# class B(BBaseFactory(static_b='1', static_b2='2').create()):
#     pass
#
#
# b = B()
# print(B.static_b)  # 'static_value'
#
#
# # Metaclass
# class BMeta:
#     def __new__(cls, name, bases, dct, static_b=None):
#         return type(name, bases, dict(**dct, static_b=static_b))
#
#
# class B(metaclass=BMeta, static_b=static_value):
#     pass
#
#
# b = B()
# print(B.static_b)  # 'static_value'
# if __name__ == '__main__':
# a = A(5)
# print(a.a)
# print(A.a)
# b = B(5)
# print(b.b)
# print(B.b)
# print(a.__kekw__)
# from operator import itemgetter
#
#
# class LoadClass:
#     @classmethod
#     def load(cls):
#         pass
#
#
# class DownloadBaseFactory: ...
# download_base_factory = DownloadBaseFactory()
#
#
# class EmbeddingTypingHelper:
#     def load(self):
#         pass
#
# class EmbeddingBaseFactory:
#     @classmethod
#     def create(cls) -> EmbeddingTypingHelper:
#         pass
#
# embedding_base_factory = EmbeddingBaseFactory()
#
#
# class RuWikiCorpora_300_10(
#     download_base_factory.create('download.com/RuWikiCorpora_300_10'),
#     embedding_base_factory.create()
# ): ...
#
# RuWikiCorpora_300_10().load()
#
#
#
# from nya_utils.functools import identity
#
# json = {
#     'id': 265722,
#     'date': 1647508974,
#     'owner_id': -77503163,
#     'from_id': 155270315,
#     'id': 265687,
#     'parents_stack': [265706],
#     'post_type': 'reply',
#     'text': '...',
#     'comments': {
#         'can_post': 0,
#         'count': 0
#     },
#     'likes': {
#         'can_like': 1,
#         'count': 0,
#         'user_likes': 0,
#         'can_publish': 1
#     },
#     'reposts': {
#         'count': 0,
#         'user_reposted': 0
#     },
#     'donut': {
#         'is_donut': False
#     },
#     'short_text_rate': 0.8
# }
#
#
# class Parser:
#     ...
#
#
# parser = Parser()
#
# parser.parse_json()
# parser.parse(id, date, owner_id, ...)
#
# parser.parse(parser.get(url))
# parser.parse_url(url)
#
#
# class _Post:
#     ...
#
#
# class Scraper:
#     def get_comments(self, post: _Post):
#         ...
#
#     def get_post_from_url(self, url) -> _Post:
#         ...
#
#     def get_post_from_json(self, js) -> _Post:
#         ...
#
#
# scraper = Scraper()
# scraper.get_comments(scraper.get_post_from_url(url))
# scraper.get_comments(scraper.get_post_from_json(json))
# from dataclasses import dataclass, replace
#
#
# @dataclass
# class Post:
#     post_id: str
#     from_id: str
#     owner_id: str
#     text: str
#
#
# if __name__ == '__main__':
#     data = {
#         'id': 'hi',
#         'owner_id': 'hi',
#         'text': 'hi',
#         'extra': 'not hi'
#     }
#     print(Post(**data))
#


# tokenizer = get_tokenizer('spacy')
#
# MAX_TOKENS = 100
#
# ru_tweet_corp_data = RuTweetCorp.load()
# ru_tweet_corp_loader = DataLoader(
#     ru_tweet_corp_data,
#     batch_size=32,
#     pad=MAX_TOKENS,
#     process=tokenizer
# )
#
# sentiment_140_ru_data = Sentiment140Ru.load(),
# sentiment_140_ru_loader = DataLoader(
#     sentiment_140_ru_data,
#     batch_size=32,
#     pad=MAX_TOKENS,
#     process=tokenizer
# )
#
# model = (
#     LSTM.builder()
#         .embedding(RuWikiVectors.load())
#         .input_dim(MAX_TOKENS)
#         .hidden_layers(3)
#         .output_dim(1)
#         .build()
# )
#
#
# trainer = Engine(model.fit)
# evaluator = Engine(model.eval)
#
# checkpointer = ModelCheckpoint('/tmp/models')
# trainer.add_event_handler(ON_EPOCHCOMPLETE, checkpointer)
#
# trainer.run(epochs=20)


import time
import multiprocessing
from operator import methodcaller


class AddDaemon(object):
    def __init__(self):
        self.stuff = 'hi there this is AddDaemon'

    def f(self):
        while True:
            print(self.stuff)
            time.sleep(3)


class RemoveDaemon(object):
    def __init__(self):
        self.stuff = 'hi this is RemoveDaemon'

    def f(self):
        while True:
            print(self.stuff)
            time.sleep(1)

def main():
    a = AddDaemon()
    r = RemoveDaemon()
    # t1 = threading.Thread(target=r.rem)
    # t2 = threading.Thread(target=a.add)
    # t1.setDaemon(True)
    # t2.setDaemon(True)
    # t1.start()
    # t2.start()
    # time.sleep(10)

    demon_pool = multiprocessing.Pool(2)
    demon_pool.map(methodcaller('f'), [a, r])
    demon_pool.join()
#     demon_pool.close()
#
# 123;print();
#
#
# list_classes('src.nya_app.nyaural_nyatworks.models')

from collections import Iterable
