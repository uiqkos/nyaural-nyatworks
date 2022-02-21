from collections import namedtuple
from dataclasses import dataclass
from functools import partial
from itertools import islice
from operator import methodcaller
from typing import Iterable

from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from nya_app.config import config
from nya_app.connectors.comments import iterate_comment_level, LabeledComment, StyledComment
from nya_app.connectors.modeladapter import ModelAdapterFactory
from nya_app.nyaural_nyatworks.admin import model_registrar as registrar
from nya_app.nyaural_nyatworks.models import Model as DBModel
from nya_app.nyaural_nyatworks.models import Report, Model
from nya_app.nyaural_nyatworks.serializers import ReportSerializer
from nya_scraping import parsers
from nya_scraping.comment import map_comment, Comment

_model_adapter_factory = ModelAdapterFactory(registrar)


def handler404(request, exception):
    return render(request, 'not_found.html', status=404)


class HomeView(TemplateView):
    template_name = 'home.html'


class ReportListView(ListView):
    model = Report
    template_name = 'reports.html'


class ReportDetailView(DetailView):
    model = Report
    queryset = Report.objects.all()

    def get(self, request, *args, **kwargs):
        report = get_object_or_404(self.model, title=kwargs['title'])
        return render(request, 'model_report.html', {'report': report})


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class PredictView(TemplateView):
    template_name = 'predict.html'
    _Group = namedtuple('Group', 'name header models')

    def get_context_data(self, **kwargs):
        context = super(PredictView, self).get_context_data(**kwargs)
        context['groups'] = [
            PredictView._Group('toxic', 'Токсичность', Model.objects.filter(target='toxic')),
            PredictView._Group('sentiment', 'Эмоциональность', Model.objects.filter(target='sentiment')),
            PredictView._Group('sarcasm', 'Саркастичность', Model.objects.filter(target='sarcasm')),
        ]

        return context


@dataclass
class Paginator:
    objects: Iterable
    per_page: int

    def page(self, number):
        number -= 1
        return islice(self.objects, number * self.per_page, number * self.per_page + self.per_page)


class CommentsView(APIView):
    def get(self, request):
        input_method = request.GET.get('input')
        text = request.GET.get('text')
        page = int(request.GET.get('page')) if 'page' in request.GET else None
        styled = bool(request.GET.get('styled')) if 'styled' in request.GET else False

        root = (
            parsers
                .get(input_method)
                .create()
                .setup(**config['parsers'][input_method])
                .parse(text)
        )

        targets = config['targets']
        model_by_target = {}

        for target in targets:
            if target in request.GET:
                db_model = (
                    DBModel.objects
                        .filter(local_name=request.GET.get(target))
                        .first()
                )
                model_by_target[target] = _model_adapter_factory.create(db_model).predict

        if page is not None:
            root = map(
                partial(LabeledComment, predictors=model_by_target),
                iterate_comment_level(root)
            )

            if styled:
                root = map(StyledComment, root)

            data = map(methodcaller('to_dict'), root)

            if page == 0:
                return Response(data=list(data))

            paginator = Paginator(data, 3)
            return Response(data=list(paginator.page(page)))

        root = map_comment(
            partial(LabeledComment, predictors=model_by_target),
            root
        )

        if styled:
            root = map_comment(StyledComment, root)

        return Response(
            data=root.to_dict()
        )


class MakePredictions(TemplateView):
    template_name = 'results.html'

    def post(self, request):
        return self.render_to_response({})


class PredictResultsView(ListView):
    def get(self, request, *args, **kwargs):
        get = QueryDict('', mutable=True)
        get.update(request.GET)
        get['page'] = 0
        get['styled'] = 1
        request.GET = get
        # request.GET = {**request.GET, 'page': 0}

        r = CommentsView().get(request)

        return render(request, 'results.html', context={'comments': r.data})

        # root = get_root_comment(request, generator=True)
        # root = map(lambda t: (StyledComment.from_predictors(t[0]), t[1]), root)
        #
        #
        #
        # paginator = Paginator(root, 3)
        # page = request.GET.get('page') if 'page' in request.GET else 1
        #
        # r = render(
        #     request=request,
        #     template_name='results.html',
        #     context={
        #         'comments': list(paginator.page(page)),
        #         # 'page': page
        #     }
        # )
        #
        # return r

    # def post()
