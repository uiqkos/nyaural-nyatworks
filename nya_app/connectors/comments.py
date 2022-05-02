from dataclasses import dataclass
from typing import Dict, Callable

from nya_scraping.comment import Comment, CommentDecorator


def NoneFactory(*args, **kwargs):
    return None


@dataclass
class LabeledComment(CommentDecorator):
    # todo: any target
    predictions: Dict[str, Dict[str, float]] = None

    def __init__(self, comment, predictions):
        super(LabeledComment, self).__init__(comment)

        self.predictions = predictions

    @classmethod
    def from_predictors(cls, comment, predictors: Dict[str, Callable[[Comment], Dict[str, float]]] = None):
        predictors = predictors or {}

        predictors = {
            **predictors
        }

        return cls(
            comment,
            {
                target: predictor(comment)
                for target, predictor in predictors.items()
            }
        )

    @property
    def attributes(self):
        return super(LabeledComment, self).attributes + ['predictions']
