import datetime
from enum import Enum

from mongoengine import *
from mongoengine_todict import DocumentMixin


class Tag(EmbeddedDocument, DocumentMixin):
    name = StringField(required=True)
    color = StringField(default='primary')


class ReportChapterItem(EmbeddedDocument, DocumentMixin):
    text = StringField(default='')
    img = StringField()  # base64 image
    table = DictField()


class ReportChapter(EmbeddedDocument, DocumentMixin):
    header = StringField(required=True)
    content = ListField(EmbeddedDocumentField(ReportChapterItem))


class Report(Document, DocumentMixin):
    title = StringField(required=True, unique=True)
    date = DateTimeField(default=datetime.datetime.now)
    chapters = ListField(EmbeddedDocumentField(ReportChapter))
    tags = ListField(EmbeddedDocumentField(Tag))


class PreprocessorStage(EmbeddedDocument, DocumentMixin):
    name = StringField(required=True)
    params = DictField()


class Preprocessor(Document, DocumentMixin):
    name = StringField()
    stages = ListField(EmbeddedDocumentField(PreprocessorStage))
    binary = BinaryField()


class Target(Enum):
    TOXIC = 'toxic'
    SARCASM = 'sarcasm'
    SENTIMENT = 'sentiment'


class Model(Document, DocumentMixin):
    name = StringField(required=True)
    struct = DynamicField()
    weights = BinaryField()
    preprocessor = ReferenceField(Preprocessor)
    target = EnumField(Target)


class Dataset(Document, DocumentMixin):
    name = StringField(required=True)
    fields = ListField(StringField())


class Train(Document, DocumentMixin):
    model = ReferenceField(Model, required=True)
    dataset = ReferenceField(Dataset, required=True)
    start_row = IntField(default=0)
    end_row = IntField()


