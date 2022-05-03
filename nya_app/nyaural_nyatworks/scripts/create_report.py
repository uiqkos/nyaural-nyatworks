import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nya_app.nyaural_nyatworks.settings')
django.setup()

from nya_app.nyaural_nyatworks.models import Report, Tag

if __name__ == '__main__':
    md = """
## Тестирование на датасетах
### Russian Language Toxic Comments from 2ch, Pikabu (Kaggle)
#### Результаты тестирования (8к комментариев, порог 0.85)
```
              precision    recall  f1-score   support

         0.0       0.90      0.98      0.94      5365
         1.0       0.95      0.79      0.86      2699

    accuracy                           0.92      8064
   macro avg       0.93      0.88      0.90      8064
weighted avg       0.92      0.92      0.91      8064
```
#### Roc кривая
![](roc_curve_kaggle_2ch_pikabu_toxic_skolkovo.png)
### Labeled comments from popular Russian social network (Kaggle)
#### Результаты тестирования (10к комментариев)
```
              precision    recall  f1-score   support

           0       0.98      1.00      0.99      8578
           1       0.99      0.91      0.95      1854

    accuracy                           0.98     10432
   macro avg       0.99      0.95      0.97     10432
weighted avg       0.98      0.98      0.98     10432
```
#### Roc кривая
![](roc_curve_kaggle_toxic_skolkovo.png)
    """

    bert_rep = Report(
        title='Russian toxicity classifier by Skolkovo Institute',
        name='SkolkovoInstitute_russian_toxicity_classifier',
        text=md,
        tags=[{'name': 'best', 'grad': 2}, {'name': 'BERT', 'grad': 1}]
    )

    bert_rep.save()
