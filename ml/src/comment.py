import json
from copy import copy
from dataclasses import dataclass, field, asdict, fields
from functools import partial
from operator import attrgetter, itemgetter
from pprint import pprint
from typing import List, Callable, Dict

from dataclasses_json import dataclass_json

from ml.utils import compose


def NoneFactory(*args, **kwargs):
    return None


@dataclass
class Author:
    name: str
    photo: str


@dataclass
class Comment:
    text: str
    author: Author = None
    date: str = None

    comments: List['Comment'] = field(default_factory=list)

    def to_dict_top_level(self):
        return {
            name: getattr(self, name)
            for name in map(attrgetter('name'), fields(self))
        }

    def to_dict(self, comments=True):
        if comments:
            return asdict(self)

        return dict(text=self.text, author=asdict(self.author), date=self.date)


@dataclass
class CommentDecorator:
    comment: Comment

    def __init__(self, comment):
        if isinstance(comment, CommentDecorator):
            self.comment = copy(comment.comment)
        elif isinstance(comment, Comment):
            self.comment = copy(comment)


@dataclass
class LabeledComment(CommentDecorator):
    sentiment: Dict[str, float] = None
    toxic: Dict[str, float] = None
    sarcasm: Dict[str, float] = None

    @classmethod
    def from_comment(
            cls,
            comment,
            predictors: Dict[str, Callable[[Comment], Dict[str, float]]] = None,
            **kwargs
    ):
        if predictors:
            predictors = {
                'toxic': NoneFactory,
                'sentiment': NoneFactory,
                'sarcasm': NoneFactory,
                **predictors
            }
        else:
            predictors = {}

        c = cls(
            comment,
            **{
                **{
                    target: predictor(comment)
                    for target, predictor in predictors.items()
                },
                **kwargs,
            }
        )

        return c


def float_color(value: float) -> 'red, green':
    red = 255 - (255 * (value < 0.5) * (1 - value * 2))
    green = 255 - (255 * (value > 0.5) * (value - 0.5) * 2)

    return red, green


@dataclass
class StyledComment(LabeledComment):
    styles: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def __post_init__(self):
        for target in ['sentiment', 'toxic', 'sarcasm']:
            values = getattr(self, target)
            label, value = '', 0
            red, green, blue = 0, 0, 0

            if not values:
                self.styles[target] = dict(
                    label='',
                    style='',
                    value=''
                )
                continue

            if len(values) == 1:
                label, value = list(values.items())[0]
                red, green = float_color(value)

            elif len(values) == 2:
                i, (label, value) = max(enumerate(values.items()), key=compose(itemgetter(1), itemgetter(1)))
                red, green = float_color(1 - value if i == 0 else value)

            elif len(values) == 3:
                i, (label, value) = max(enumerate(values.items()), key=compose(itemgetter(1), itemgetter(1)))
                if i == 1:
                    value /= 2
                    red, green, blue = 0, 0, 255

                elif i == 2:
                    red, green = float_color(value)

                else:
                    red, green = float_color(1 - value)

            color = 'white' if red > 100 else 'black'
            color = 'white' if blue else color

            self.styles[target] = dict(
                label=label,
                style=f'background-color: rgb({red}, {green}, {blue}); color: {color}',
                value=f'{int(value * 100)}%'
            )


@dataclass_json
@dataclass
class CommentOneDim(CommentDecorator):
    level: int = 0



def map_comment(comment, func: Callable[[Comment], Comment]) -> Comment:
    comments = copy(comment.comments)

    comment = func(comment)
    comment.comments = list(map(partial(map_comment, func=func), comments))

    return comment


def map_comment_attr(comment, attr: str, func: Callable[[Comment], object]) -> Comment:
    def setter(c):
        setattr(c, attr, func(c))
        return c
    return map_comment(comment, setter)


def iterate_comment_level(comment: Comment, level=0):
    c = CommentOneDim(comment, level=level)
    # c.comments = []
    yield c

    for c1 in comment.comments:
        for c2 in iterate_comment_level(c1, level=level + 1):
            yield c2


if __name__ == '__main__':
    c_ = Comment(
        '1', comments=[
            Comment('1.1'),
            Comment(
                '1.2',
                comments=[
                    Comment(
                        '1.2.1',
                        comments=[
                            Comment('1.2.1.1'),
                            Comment('1.2.1.2'),
                            Comment('1.2.1.3'),
                        ]
                    )
                ]
            ),
            Comment('1.3')]
    )

    for c in iterate_comment_level(StyledComment(c_)):
        print(c.to_json())

    # lc = LabeledComment.from_comment(c_, sentiment={'positive': 100})
    # print(json.dumps(lc.to_dict(), indent=4))

    # mapper = partial(LabeledComment.from_comment, predictors={'toxic': NoneFactory}, sentiment={'positive': 100})
    #
    # lc = map_comment(c_, mapper)
    #
    # print(json.dumps(lc.to_dict(), indent=4))
    # print(lc.to_dict())