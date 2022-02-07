from collections import namedtuple
from functools import partial
from typing import Dict

import target as target
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework.viewsets import ModelViewSet

import nyaural_nyatworks
from config import config
from ml.src import parsers, models
from ml.src.comment import Comment
from nyaural_nyatworks.models import Report, Model
from nyaural_nyatworks.serializers import ReportSerializer


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


class PredictResultsView(ListView):
    def get(self, request, *args, **kwargs):
        input_method = request.GET.get('input')
        text = request.GET.get('text')

        comments = (
            parsers
                .get(input_method)
                .default_setup()
                .parse(text)
        )

        targets = config['targets']
        models_by_target = {}

        for target in targets:
            local_model_name = (
                nyaural_nyatworks.models.Model.objects
                    .filter(name=request.GET.get(target))
                    .first()
                    .local_name
            )
            models_by_target[target] = models.get(local_model_name, target).load()

        map_comment(comments, models_by_target)

        return render(request, 'results.html', {'comments': comments.to_dict()})


def map_comment(comment: Comment, models: Dict[str, models.Model]):
    comment.toxic = models['toxic'].predict(comment)
    comment.sentiment = models['sentiment'].predict(comment)
    comment.sarcasm = models['sarcasm'].predict(comment)

    comment.comments = list(map(partial(map_comment, models=models), comment.comments))

    return comment
