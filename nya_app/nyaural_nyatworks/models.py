from datetime import datetime
from typing import List, Union

from django.forms import Form, ModelForm
from djongo.models import (
    # Model as AbstractDBModel,
    Model as DBModel,
    TextField,
    DateTimeField,
    ArrayField,
    JSONField,
    IntegerField,
    ObjectIdField,
    OneToOneField,
    URLField,
    CASCADE,
    EmbeddedField,
    ArrayReferenceField,
    DjongoManager
)


# class AbstractDBModel(DBModel):
#     id = ObjectIdField()
#
#     class Meta:
#         abstract = True


class Tag(DBModel):
    name = TextField()
    grad = IntegerField()

    class Meta:
        abstract = True

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'grad')


class Report(DBModel):
    name: str = TextField(primary_key=True)
    title: str = TextField()
    date: datetime = DateTimeField(auto_now=True)
    text: str = TextField()
    tags: List[Tag] = ArrayField(Tag, model_form_class=TagForm, default=list)

    objects = DjongoManager()


class Model(DBModel):
    local_name = TextField(primary_key=True, unique=True)
    name = TextField(null=False)
    struct = JSONField(null=True)
    target = TextField()

    objects = DjongoManager()

