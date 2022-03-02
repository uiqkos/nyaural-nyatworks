from dataclasses import dataclass, field
from operator import itemgetter
from typing import Dict, Callable

from nya_scraping.comment import Comment, CommentDecorator
from nya_utils.functools import compose


@dataclass
class CommentOneDim(CommentDecorator):
    comments: int = 0
    level: int = 0

    def __init__(self, comment, level=0):
        super().__init__(comment)

        self.level = level
        self.comments = len(comment.comments)

    @property
    def attributes(self):
        return super(CommentOneDim, self).attributes + ['level']

    def to_dict(self, comments=True):
        return {
            **super(CommentOneDim, self).to_dict(False),
            'comments': self.comments,
        }

    def __len__(self):
        return 1 + self.comments


def iterate_comment_level(comment: Comment, level=0):
    yield CommentOneDim(comment, level=level)

    for c1 in comment.comments:
        for c2 in iterate_comment_level(c1, level=level + 1):
            yield c2


def NoneFactory(*args, **kwargs):
    return None


@dataclass
class LabeledComment(CommentDecorator):
    # todo: any target
    sentiment: Dict[str, float] = None
    toxic: Dict[str, float] = None
    sarcasm: Dict[str, float] = None

    def __init__(self, comment, toxic=None, sentiment=None, sarcasm=None):
        super().__init__(comment)

        self.toxic = toxic
        self.sentiment = sentiment
        self.sarcasm = sarcasm

    @classmethod
    def from_predictors(cls, comment, predictors: Dict[str, Callable[[Comment], Dict[str, float]]] = None):
        predictors = predictors or {}

        predictors = {
            'toxic': NoneFactory,
            'sentiment': NoneFactory,
            'sarcasm': NoneFactory,
            **predictors
        }

        return cls(
            comment,
            **{
                target: predictor(comment)
                for target, predictor in predictors.items()
            }
        )

    @property
    def attributes(self):
        return super(LabeledComment, self).attributes + ['sentiment', 'toxic', 'sarcasm']


def float_color(value: float) -> 'red, green':
    red = 255 - (255 * (value < 0.5) * (1 - value * 2))
    green = 255 - (255 * (value > 0.5) * (value - 0.5) * 2)

    return red, green


@dataclass
class StyledComment(CommentDecorator):
    styles: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def __init__(self, comment: LabeledComment):
        super().__init__(comment)

        self.styles = {}
        self.__post_init__()

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

    @property
    def attributes(self):
        return super(StyledComment, self).attributes + ['styles']
