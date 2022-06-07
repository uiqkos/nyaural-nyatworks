from dataclasses import make_dataclass, dataclass
from functools import partial
from itertools import cycle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scikitplot.metrics import plot_roc

from nya_ml_research.config import DATA_PATH
from nya_utils.path import file_paths


colors = cycle(['blue', 'green'])


def roc_curve(dataset_name, model_name, filepath, classes=(), **kwargs):
    df = pd.read_csv(filepath)
    y_true, y_pred_all_labels = df.y_true, df.iloc[:, 2:]

    roc = plot_roc(
        y_true, y_pred_all_labels,
        title=dataset_name,
        plot_macro=True,
        classes_to_plot=classes,
        plot_micro=False,
        macro_title=model_name,
        # macro_color=next(colors),
        **kwargs
    )

def plot_by_dataset():
    Curves = make_dataclass('Curves', ['fig', 'ax'])
    curves_by_ds = {}

    ds = 'Russian language toxic comments from Kaggle'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_skolkovorutoxicityclassifier_dataset_get_russian_language_toxic_comments.csv',
         'Skolkovo'),
        (DATA_PATH / 'reports' / 'model_sismetaninruberttoxic_dataset_get_russian_language_toxic_comments.csv',
         'Sismetanin')
    ]:
        curves = curves_by_ds.setdefault(ds, Curves(*plt.subplots(1, 1)))
        roc_curve(ds, mname, fp, ax=curves.ax)
    curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '.png')

    ds = 'Russian toxic comments from Kaggle'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_skolkovorutoxicityclassifier_dataset_get_toxic_russian_comments.csv',
         'Skolkovo'),
        (DATA_PATH / 'reports' / 'model_sismetaninruberttoxic_dataset_get_toxic_russian_comments.csv', 'Sismetanin')
    ]:
        curves = curves_by_ds.setdefault(ds, Curves(*plt.subplots(1, 1)))
        roc_curve(ds, mname, fp, ax=curves.ax)
    curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '.png')

    ds = 'Sentiment Analysis in Russian from Kaggle'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_blanchefortrubertsentiment_dataset_get_kaggle_news.csv', 'Blanchefort'),
        (DATA_PATH / 'reports' / 'model_tatyanarubertsentiment_dataset_get_kaggle_news.csv', 'Tatyana')
    ]:
        curves = curves_by_ds.setdefault(ds, Curves(*plt.subplots(1, 1)))
        roc_curve(ds, mname, fp, ax=curves.ax)
    curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '.png')

    ds = 'RuSentiment'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_blanchefortrubertsentiment_dataset_get_rusentiment.csv', 'Blanchefort'),
        (DATA_PATH / 'reports' / 'model_tatyanarubertsentiment_dataset_get_rusentiment.csv', 'Tatyana')
    ]:
        curves = curves_by_ds.setdefault(ds, Curves(*plt.subplots(1, 1)))
        roc_curve(ds, mname, fp, ax=curves.ax)
    curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '.png')

    # for curve in curves_by_ds.values():
    #     curve


def plot_by_model():
    Curves = make_dataclass('Curves', ['fig', 'ax'])
    curves_by_ds = {}

    ds = 'Russian language toxic comments from Kaggle'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_skolkovorutoxicityclassifier_dataset_get_russian_language_toxic_comments.csv',
         'Skolkovo'),
        (DATA_PATH / 'reports' / 'model_sismetaninruberttoxic_dataset_get_russian_language_toxic_comments.csv',
         'Sismetanin')
    ]:
        curves = Curves(*plt.subplots(1, 1))
        roc_curve(ds, mname, fp, classes=(0, 1), ax=curves.ax)
        curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '_model_' + mname + '.png')

    ds = 'Russian toxic comments from Kaggle'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_skolkovorutoxicityclassifier_dataset_get_toxic_russian_comments.csv',
         'Skolkovo'),
        (DATA_PATH / 'reports' / 'model_sismetaninruberttoxic_dataset_get_toxic_russian_comments.csv', 'Sismetanin')
    ]:
        curves = Curves(*plt.subplots(1, 1))
        roc_curve(ds, mname, fp, classes=(0, 1), ax=curves.ax)
        curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '_model_' + mname + '.png')

    ds = 'Sentiment Analysis in Russian from Kaggle'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_blanchefortrubertsentiment_dataset_get_kaggle_news.csv', 'Blanchefort'),
        (DATA_PATH / 'reports' / 'model_tatyanarubertsentiment_dataset_get_kaggle_news.csv', 'Tatyana')
    ]:
        curves = Curves(*plt.subplots(1, 1))
        roc_curve(ds, mname, fp, classes=(0, 1, 2), ax=curves.ax)
        curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '_model_' + mname + '.png')

    ds = 'RuSentiment'
    for fp, mname in [
        (DATA_PATH / 'reports' / 'model_blanchefortrubertsentiment_dataset_get_rusentiment.csv', 'Blanchefort'),
        (DATA_PATH / 'reports' / 'model_tatyanarubertsentiment_dataset_get_rusentiment.csv', 'Tatyana')
    ]:
        curves = Curves(*plt.subplots(1, 1))
        roc_curve(ds, mname, fp, classes=(0, 1, 2), ax=curves.ax)
        curves.ax.get_figure().savefig(ds.lower().replace(' ', '_') + '_model_' + mname + '.png')

    # for curve in curves_by_ds.values():
    #     curve


if __name__ == '__main__':
    plot_by_model()
