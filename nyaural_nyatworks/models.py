from dataclasses import dataclass
from datetime import datetime
from typing import List, Union

from djongo.models import (
    # Model as AbstractDBModel,
    Model as DBModel,
    TextField,
    DateTimeField,
    ArrayField,
    BinaryField,
    JSONField,
    IntegerField,
    ObjectIdField,
    OneToOneField,
    URLField,
    UUIDField,
    CASCADE
)


class AbstractDBModel(DBModel):
    id = ObjectIdField()

    class Meta:
        abstract = True


class Tag(AbstractDBModel):
    name = TextField()
    color = TextField(default='primary')


class ReportChapterItem(AbstractDBModel):
    text: str = TextField()
    img: str = TextField(null=True)  # base64 image
    table: Union[dict, list] = JSONField(null=True)


class ReportChapter(AbstractDBModel):
    header: str = TextField()
    content: List[ReportChapterItem] = ArrayField(ReportChapterItem)


class Report(AbstractDBModel):
    title: str = TextField()
    date: datetime = DateTimeField(auto_now=True)
    chapters: List[ReportChapter] = ArrayField(ReportChapter)
    tags: List[Tag] = ArrayField(Tag, null=True)


class PreprocessorStage(AbstractDBModel):
    name = TextField()
    params = JSONField(null=True)


class Preprocessor(AbstractDBModel):
    name = TextField()
    stages = ArrayField(PreprocessorStage)
    binary = BinaryField(null=True)


TARGET_CHOICES = (
    ('TOXIC', 'toxic'),
    ('SARCASM', 'sarcasm'),
    ('SENTIMENT', 'sentiment'),
)


class Model(AbstractDBModel):
    name = TextField(null=False)
    struct = JSONField(null=True)
    weights = BinaryField(null=True)
    preprocessor = OneToOneField(Preprocessor, on_delete=CASCADE)
    target = TextField(choices=TARGET_CHOICES)
    local_name = TextField()


DATASET_SOURCE_CHOICES = (
    ('KAGGLE', 'kaggle'),
    ('OTHER', 'other'),
)


class Dataset(AbstractDBModel):
    name = TextField(null=False)
    fields = JSONField()
    target = TextField(choices=TARGET_CHOICES)
    link = URLField(null=True)
    source = TextField(choices=DATASET_SOURCE_CHOICES)
    download_link = URLField(null=True)


class Train(AbstractDBModel):
    model = OneToOneField(Model, primary_key=False, on_delete=CASCADE)
    dataset = OneToOneField(Dataset, primary_key=False, on_delete=CASCADE)
    start_row = IntegerField(default=0)
    end_row = IntegerField(null=True)


