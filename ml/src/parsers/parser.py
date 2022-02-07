from abc import ABC
from datetime import datetime

from ml.src.comment import Comment


class Parser:
    def parse(self, inputs) -> Comment:
        return Comment(author='', date=datetime.now().strftime('%Y-%m-%d'), text=inputs)

    def setup(self, *args, **kwargs):
        return self

    def default_setup(self):
        return self
