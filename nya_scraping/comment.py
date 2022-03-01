from copy import copy
from dataclasses import field, dataclass, asdict
from functools import partial
from typing import List, Callable


@dataclass
class Author:
    name: str
    photo: str

# todo add likes
@dataclass
class Comment:
    text: str
    author: Author = None
    date: str = None

    comments: List['Comment'] = field(default_factory=list)

    @classmethod
    @property
    def empty(cls):
        return cls('')

    @property
    def attributes(self):
        return ['text', 'author', 'date', 'comments']

    def to_dict(self, comments=True):
        d = {
            'text': self.text,
            'author': asdict(self.author) if self.author else None,
            'date': self.date
        }

        if comments:
            return {
                **d, 'comments': [comment.to_dict() for comment in self.comments]
            }

        return d

    def __len__(self):
        return 1 + sum(map(len, self.comments))


@dataclass
class CommentDecorator(Comment):
    _comment: Comment = None

    @property
    def comment(self):
        return self._comment

    def __init__(self, comment):
        self._comment = comment

    @property
    def attributes(self):
        return self._comment.attributes

    def __getattr__(self, item):
        if item in self._comment.attributes:
            return getattr(self._comment, item)
        return self.__dict__[item]

    def to_dict(self, comments=True):
        return {
            **{
                attr: getattr(self, attr)
                for attr in self.attributes
                if attr != 'comments'
            },
            **self._comment.to_dict(comments)
        }


def map_comment(func: Callable[[Comment], Comment], comment):
    comments = copy(comment.comments)

    comment = func(comment)
    comment.comments = list(map(partial(map_comment, func), comments))

    return comment
