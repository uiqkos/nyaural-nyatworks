import datetime

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

