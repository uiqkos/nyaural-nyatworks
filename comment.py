from dataclasses import dataclass, field
from typing import List


# class Comment(abc.ABC):
#     @property
#     @abstractmethod
#     def comments(self):
#         pass
#
#     @property
#     @abstractmethod
#     def text(self):
#         pass
#
#     @property
#     @abstractmethod
#     def predictions(self):
#         pass
#
#     def to_html(self, parent=None):
#         if parent is None:
#             doc, tag, text = Doc().tagtext()
#         else:
#             doc, tag, text = parent.tagtext()
#
#         if len(self.comments) == 0:
#             if parent is not None:
#                 return text(self.text)
#             return self.text
#
#         text(self.text)
#         with tag('ul', klass='list-group' + ' nested' * (parent is None)):
#             for comment in self.comments:
#                 with tag('li', klass='list-group-item'):
#                     comment.to_html(parent=doc)
#
#         if parent is None:
#             return doc.getvalue()
#         return doc


@dataclass
class Comment:
    author: str
    text: str
    likes: int = 0
    comments: List = field(default_factory=list)


# @dataclass
# class CommentWithPrediction:
#     text: str
#     toxic_emoji: str
#     comments: List = field(default_factory=list)

