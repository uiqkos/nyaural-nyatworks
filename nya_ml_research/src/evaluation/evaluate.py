import gc
import json
from functools import partial
from itertools import islice
from typing import Iterable, Tuple

import pandas as pd
import torch
from sklearn.metrics import classification_report
from sklearn.utils import gen_batches
from tqdm import tqdm

from nya_ml.models import *
from nya_ml_research.config import DATA_PATH
from nya_ml_research.src.evaluation.datasets import get_rusentiment, get_kaggle_news, \
    get_russian_language_toxic_comments, get_toxic_russian_comments

BATCH_SIZE = 32

sentiment_model_suppliers = [
    partial(TatyanaRuBertSentiment.load, 'cuda'),
    partial(BlanchefortRuBertSentiment.load, 'cuda'),
]

toxic_model_suppliers = [
    partial(SismetaninRuBertToxic.load, 'cuda'),
    partial(SkolkovoRuToxicityClassifier.load, 'cuda'),
]

sentiment_dataset_suppliers = [get_rusentiment, get_kaggle_news]
toxic_dataset_suppliers = [get_russian_language_toxic_comments, get_toxic_russian_comments]


def clear(assert_cuda=False):
    gc.collect()

    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    gc.collect()

    if assert_cuda:
        assert torch.cuda.memory_allocated() == 0, 'Can`t clear memory'


def evaluate(dataset, model):
    y_pred = torch.empty(0)
    y_pred_all_labels = torch.empty(0, len(model.grad))
    y_true = []

    for batch in tqdm(gen_batches(len(dataset), BATCH_SIZE), total=int(len(dataset) / BATCH_SIZE)):
        predicted = model._predict(dataset.text[batch].tolist())
        y_pred_all_labels = torch.cat([y_pred_all_labels, predicted])
        y_pred = torch.cat([y_pred, torch.argmax(predicted, dim=1)])
        y_true += dataset.label[batch].tolist()

    y_pred = y_pred.tolist()

    return y_true, y_pred, y_pred_all_labels


def get_models_errors(
    dataset,
    model,
    incorrect_max_count=10,
    correct_max_count=0
) -> Iterable[Tuple[bool, str, int, int, float]]:

    incorrect_count = 0
    correct_count = 0

    for batch in tqdm(gen_batches(len(dataset), BATCH_SIZE), total=int(len(dataset) / BATCH_SIZE)):
        predicted = model._predict(dataset.text[batch].tolist())
        y_pred = torch.argmax(predicted, dim=1).tolist()

        for text, true, pred_label, pred_prop in zip(
            dataset.text[batch],
            dataset.label[batch],
            y_pred,
            map(list.__getitem__, predicted.tolist(), y_pred)
        ):
            if pred_label != true:
                if incorrect_count < incorrect_max_count:
                    yield False, text, true, pred_label, pred_prop
                    incorrect_count += 1
            elif correct_count < correct_max_count:
                yield True, text, true, pred_label, pred_prop
                correct_count += 1

        if correct_count >= correct_max_count and incorrect_count >= incorrect_max_count:
            return


def examples(
    model_suppliers,
    dataset_suppliers
):
    for model_supplier in model_suppliers:
        model = model_supplier()
        print(f'Model loaded (cuda: {round(torch.cuda.memory_allocated() / 1024 ** 2)} MB)')

        for dataset_supplier in dataset_suppliers:
            key = f'Model: {model.__class__.__name__} Dataset: {dataset_supplier.__name__}'
            print(key)
            key = key.lower().replace(':', '').replace(' ', '_')

            ds = dataset_supplier()

            correct = []
            incorrect = []

            for is_correct, text, true, pred_label, pred_prop in get_models_errors(ds, model, 100, 100):
                res = {
                    'text': text,
                    'true': list(model.grad.keys())[true],
                    'predicted': f'{list(model.grad.keys())[pred_label]} {int(pred_prop * 100)}%'
                }

                if is_correct:
                    correct.append(res)
                else:
                    incorrect.append(res)

            with open(DATA_PATH / 'reports' / (key + '.examples.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'correct': correct, 'incorrect': incorrect
                }, f, ensure_ascii=False, indent=4)

        del model
        clear(assert_cuda=True)




def clf_reports(
    model_suppliers,
    dataset_suppliers
):
    for model_supplier in model_suppliers:
        model = model_supplier()
        print(f'Model loaded (cuda: {round(torch.cuda.memory_allocated() / 1024 ** 2)} MB)')

        for dataset_supplier in dataset_suppliers:
            print('before:', before := torch.cuda.memory_allocated())

            key = f'Model: {model.__class__.__name__} Dataset: {dataset_supplier.__name__}'
            print(key)
            key = key.lower().replace(':', '').replace(' ', '_')

            ds = dataset_supplier()

            y_true, y_pred, y_pred_all_labels = evaluate(ds, model)

            pd.DataFrame({
                'y_true': y_true,
                'y_pred': y_pred,
                **dict(zip(model.grad.keys(), y_pred_all_labels.T.tolist()))
            }).applymap(lambda x: round(x, 5)).to_csv(DATA_PATH / 'reports' / (key + '.csv'), index=False)

            clf_report = classification_report(y_true, y_pred, digits=2)

            print(clf_report)

            with open(DATA_PATH / 'reports' / (key + '.clf_report.txt'), 'w') as f:
                f.write(clf_report)

            print('after:', after := torch.cuda.memory_allocated())
            print()

            assert before == after

        del model
        clear(assert_cuda=True)


if __name__ == '__main__':
    # clf_reports(sentiment_model_suppliers, sentiment_dataset_suppliers)
    # clf_reports(toxic_model_suppliers, toxic_dataset_suppliers)

    examples(sentiment_model_suppliers, sentiment_dataset_suppliers)
    examples(toxic_model_suppliers, toxic_dataset_suppliers)
