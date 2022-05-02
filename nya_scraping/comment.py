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
    comments: int = 0

    @property
    def attributes(self):
        return ['id', 'text', 'author', 'date']

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': asdict(self.author) if self.author else None,
            'date': self.date,
            'comments': self.comments,
        }


@dataclass
class CommentDecorator(Comment):
    _comment: Comment = None

    @property
    def comment(self):
        return self._comment

    def __init__(self, comment):
        self.__dict__['_comment'] = comment

    @property
    def attributes(self):
        return self._comment.attributes

    def __getattribute__(self, item):
        comment = object.__getattribute__(self, '_comment')
        if comment is not None and item in comment.attributes:
            return getattr(comment, item)
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        if self.__dict__['_comment'] is not None and key in self._comment.attributes:
            setattr(self._comment, key, value)
        else:
            self.__dict__[key] = value

    def to_dict(self):
        return {
            **{
                attr: getattr(self, attr)
                for attr in self.attributes
            },
            **self._comment.to_dict()
        }

@dataclass
class CommentOneDim(CommentDecorator):
    level: int = 0

    def __init__(self, comment, level=0):
        super(CommentOneDim, self).__init__(comment)

        self.level = level

    @property
    def attributes(self):
        return super(CommentOneDim, self).attributes + ['level']

