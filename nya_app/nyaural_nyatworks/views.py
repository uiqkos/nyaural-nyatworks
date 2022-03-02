from collections import namedtuple
from dataclasses import dataclass
from functools import partial
from itertools import islice
from operator import methodcaller, itemgetter
from statistics import mean
from typing import Iterable

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from nya_app.config import config
from nya_app.connectors.comments import iterate_comment_level, LabeledComment, StyledComment
from nya_app.connectors.modeladapter import ModelAdapterFactory
from nya_app.connectors.parserfactory import ParserFactory
from nya_app.nyaural_nyatworks.admin import model_registrar as registrar
from nya_app.nyaural_nyatworks.models import Model as DBModel
from nya_app.nyaural_nyatworks.models import Report, Model
from nya_app.nyaural_nyatworks.serializers import ReportSerializer, ModelSerializer
from nya_scraping.comment import map_comment, Comment
from nya_utils.functools import compose, get_item_or

_model_adapter_factory = ModelAdapterFactory(registrar)
_parser_factory = ParserFactory(config['parsers'])


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ModelViewSet(ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


@dataclass
class Paginator:
    objects: Iterable
    per_page: int = -1

    def page(self, number=1):
        if self.per_page == -1:
            return self.objects
        number -= 1
        return islice(self.objects, number * self.per_page, number * self.per_page + self.per_page)


class CommentsView(APIView):
    def get(self, request):
        input_method = request.GET.get('input')
        text = request.GET.get('text')
        page = get_item_or(request.GET, 'page', default=None, astype=int)
        # page = int(request.GET.get('page')) if 'page' in request.GET else None
        styled = get_item_or(request.GET, 'styled', default=False)
        # styled = bool(request.GET.get('styled')) if 'styled' in request.GET else False
        per_page = get_item_or(request.GET, 'per_page', default=3)
        # per_page = int(request.GET.get('per_page')) if 'per_page' in request.GET else 3
        stats = get_item_or(request.GET, 'stats', default=False)
        # stats = bool(request.GET.get('stats')) if 'stats' in request.GET else False

        root = (
            _parser_factory
                .create(input_method, text)
                .parse(text)
        )

        targets = [
            target for target in config['targets']
            if target in request.GET and request.GET.get(target) not in ('', None)
        ]
        model_by_target = {}

        for target in targets:
            db_model = (
                DBModel.objects
                    .filter(local_name=request.GET.get(target))
                    .first()
            )
            model_by_target[target] = _model_adapter_factory.create(db_model).predict

        if page is not None:
            root = map(
                partial(LabeledComment.from_predictors, predictors=model_by_target),
                iterate_comment_level(root)
            )

            if styled:
                root = map(StyledComment, root)

            data = map(methodcaller('to_dict'), root)
            paginator = Paginator(data, per_page if page else -1)
            items = list(paginator.page(page))

            if stats:
                stats = {}

                for target in targets:
                    stats[target] = {
                        key: mean(map(compose(itemgetter(target), itemgetter(key)), items))
                        for key in items[0][target].keys()
                    }

                stats = LabeledComment(Comment.empty, **stats)
                stats = StyledComment(stats)
                stats = {'styles': stats.styles}

            else:
                stats = {}

            return Response(data={
                'items': items,
                'count': len(items),
                **stats
            })

        root = map_comment(
            partial(LabeledComment.from_predictors, predictors=model_by_target),
            root
        )

        if styled:
            root = map_comment(StyledComment, root)

        return Response(data={
            'items': [root.to_dict()],
            'pages': 1,
            'per_page': 1,
            'found': 1
        })
