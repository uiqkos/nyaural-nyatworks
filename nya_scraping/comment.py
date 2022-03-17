from dataclasses import dataclass, asdict


@dataclass(unsafe_hash=True)
class Author:
    name: str
    photo: str


# todo add likes
@dataclass
class Comment:
    text: str
    author: Author = None
    date: str = None
    id: str = None

    @property
    def attributes(self):
        return ['id', 'text', 'author', 'date']

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': asdict(self.author) if self.author else None,
            'date': self.date
        }


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

    def __getattribute__(self, item):
        comment = object.__getattribute__(self, '_comment')
        if item in comment.attributes:
            return getattr(comment, item)
        return object.__getattribute__(self, item)

    def to_dict(self):
        return {
            **{
                attr: getattr(self, attr)
                for attr in self.attributes
            },
            **self._comment.to_dict()
        }
