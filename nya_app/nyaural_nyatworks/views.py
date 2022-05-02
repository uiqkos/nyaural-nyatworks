import math
from dataclasses import dataclass, asdict
from functools import partial
from itertools import islice
from operator import methodcaller, itemgetter
from statistics import mean
from typing import List, Dict

import kwargs as kwargs
from more_itertools import minmax
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from nya_app.config import config
from nya_app.connectors.comments import LabeledComment
from nya_app.connectors.modeladapterfactory import ModelAdapterFactory
from nya_app.connectors.scraperfactory import ScraperFactory
from nya_app.nyaural_nyatworks.admin import model_registrar as registrar
from nya_app.nyaural_nyatworks.models import Model as DBModel
from nya_app.nyaural_nyatworks.models import Report
from nya_app.nyaural_nyatworks.serializers import ReportSerializer, ModelSerializer
from nya_scraping.comment import Comment
from nya_utils.datatools import filter_dataclass_kwargs, cast_arguments, filter_dict
from nya_utils.functools import compose

_model_adapter_factory = ModelAdapterFactory(registrar)
_scraper_factory = ScraperFactory(config['scrapers'])


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ModelViewSet(ModelViewSet):
    queryset = DBModel.objects.all()
    serializer_class = ModelSerializer


@cast_arguments
@dataclass
class PredictRequestParams:
    text: str
    input: str = 'auto'
    page: int = 0
    per_page: int = 3
    styled: bool = False
    stats: bool = False
    expand: str = None
    expand_path: list = None

    def __post_init__(self):
        if self.expand:
            self.expand_path = self.expand.removesuffix('/').removeprefix('/').split('/')
        else:
            self.expand = ''


class CommentsView(APIView):
    def get(self, request):
        params_kwargs, extra = filter_dataclass_kwargs(
            PredictRequestParams, request.GET, return_tuple=True)

        local_name_by_target, create_kwargs = filter_dict(
            config['targets'], extra, return_tuple=True)

        params = PredictRequestParams(**params_kwargs)
        scraper = _scraper_factory.create(params.input, params.text, **create_kwargs)

        comments = scraper.get_comments(
            params.text,
            path=params.expand_path
        )

        model_by_target = {}
        model_name_by_target = {}

        for target, local_name in local_name_by_target.items():
            db_model = (
                DBModel.objects
                    .filter(local_name=local_name)
                    .first()
            )

            if db_model is None:
                continue

            model_name_by_target[target] = db_model.local_name
            model_by_target[target] = _model_adapter_factory.create(db_model)

        comments = map(
            partial(LabeledComment.from_predictors, predictors=model_by_target),
            comments
        )

        comments = map(methodcaller('to_dict'), comments)

        if not params.page:
            items = list(comments)
        else:
            items = list(islice(
                comments,
                start := (params.page - 1) * params.per_page,
                start + params.per_page
            ))

        stats = params.stats

        if stats:
            mean_min_max_by_target = {}

            for target in model_by_target.keys():
                mean_min_max_by_target[target] = {}

                for name in items[0]['predictions'][target].keys():
                    values = list(map(
                        compose(
                            itemgetter('predictions'),
                            itemgetter(target),
                            itemgetter(name)
                        ),
                        items
                    ))

                    mean_min_max_by_target[target][name] = {
                        'mean': mean(values),
                        **dict(zip(['min', 'max'], minmax(values)))
                    }

            stats = mean_min_max_by_target

        return Response(data=dict(
            models=model_name_by_target,
            grads=dict(map(lambda t: (t[0], t[1].grad), model_by_target.items())),
            items=items,
            path=params.expand + '/',
            per_page=params.per_page,
            page=params.page,
            count=len(items),
            **({'stats': stats} if stats else {})
        ))
