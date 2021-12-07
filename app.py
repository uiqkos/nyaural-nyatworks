import dataclasses
from random import randint

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from comment import Comment
from ml import *

# from report import Report

app = Flask(__name__)
bootstrap = Bootstrap(app)

toxic_model = load_toxic_model()

simple_comment = Comment(
    author='Uiqkos',
    text='Hello, guys!',
    comments=[
        Comment(
            author='LostMan',
            text='Hi!',
            likes=1,
            comments=[
                Comment(
                    author='Uiqkos',
                    text='Nice'
                )
            ]
        ),
        Comment(
            author='C#ovasecaichi',
            text='Good morning',
            likes=34,
            comments=[
                Comment(
                    author='Uiqkos',
                    text='Yes',
                ),
                Comment(
                    author='LostMan',
                    text='let me die'
                ),
            ]
        )
    ]
)


# example_report = Report(
#     name='Heavy CNN',
#     description='Heavy CNN with 10 hidden_layers',
#     scores={
#         'loss': '0.02',
#         'accuracy': '98.981'
#     }
# )


def make_prediction(comment):
    return dict(
        author=comment.author,
        text=comment.text,
        emoji=toxic_model.predict([randint(0, 1) for _ in range(6)]).emoji,
        comments=list(map(make_prediction, comment.comments))
    )


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/results')
def results():
    return render_template(
        'results.html',
        comments=make_prediction(simple_comment)
    )


@app.route('/report/<int:report_id>')
def get_report(report_id: int):
    from base64 import b64encode
    from .report import ModelReport

    with open('./res/example_model.png', 'rb') as f:
        b64img = b64encode(f.read()).decode('utf-8')

    return render_template(
        'model_report.html',
        **dataclasses.asdict(ModelReport(
            model_name='Large CNN',
            desc='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor '
                 'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
                 'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo '
                 'consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum '
                 'dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, '
                 'sunt in culpa qui officia deserunt mollit anim id est laborum.',
            arch_desc='В обычном перцептроне, который представляет собой полносвязную нейронную сеть, '
                      'каждый нейрон связан со всеми нейронами предыдущего слоя, причём каждая связь имеет свой '
                      'персональный весовой коэффициент. В свёрточной нейронной сети в операции свёртки '
                      'используется лишь ограниченная матрица весов небольшого размера, которую «двигают» по всему '
                      'обрабатываемому слою (в самом начале — непосредственно по входному изображению), '
                      'формируя после каждого сдвига сигнал активации для нейрона следующего слоя с аналогичной '
                      'позицией. То есть для различных нейронов выходного слоя используются одна и та же матрица '
                      'весов, которую также называют ядром свёртки. Её интерпретируют как графическое кодирование '
                      'какого-либо признака, например, наличие наклонной линии под определённым углом. Тогда '
                      'следующий слой, получившийся в результате операции свёртки такой матрицей весов, '
                      'показывает наличие данного признака в обрабатываемом слое и её координаты, формируя так '
                      'называемую карту признаков (англ. feature map). Естественно, в свёрточной нейронной сети '
                      'набор весов не один, а целая гамма, кодирующая элементы изображения (например линии и дуги '
                      'под разными углами). При этом такие ядра свёртки не закладываются исследователем заранее, '
                      'а формируются самостоятельно путём обучения сети классическим методом обратного '
                      'распространения ошибки. Проход каждым набором весов формирует свой собственный экземпляр '
                      'карты признаков, делая нейронную сеть многоканальной (много независимых карт признаков на '
                      'одном слое). Также следует отметить, что при переборе слоя матрицей весов её передвигают '
                      'обычно не на полный шаг (размер этой матрицы), а на небольшое расстояние. Так, например, '
                      'при размерности матрицы весов 5×5 её сдвигают на один или два нейрона (пикселя) вместо '
                      'пяти, чтобы не «перешагнуть» искомый признак. Операция субдискретизации (англ. subsampling, '
                      'англ. pooling, также переводимая как «операция подвыборки» или операция объединения), '
                      'выполняет уменьшение размерности сформированных карт признаков. В данной архитектуре сети '
                      'считается, что информация о факте наличия искомого признака важнее точного знания его '
                      'координат, поэтому из нескольких соседних нейронов карты признаков выбирается максимальный '
                      'и принимается за один нейрон уплотнённой карты признаков меньшей размерности. За счёт '
                      'данной операции, помимо ускорения дальнейших вычислений, сеть становится более инвариантной '
                      'к масштабу входного изображения. Рассмотрим типовую структуру свёрточной нейронной сети '
                      'более подробно. Сеть состоит из большого количества слоёв. После начального слоя (входного '
                      'изображения) сигнал проходит серию свёрточных слоёв, в которых чередуется собственно '
                      'свёртка и субдискретизация (пулинг). Чередование слоёв позволяет составлять «карты '
                      'признаков» из карт признаков, на каждом следующем слое карта уменьшается в размере, '
                      'но увеличивается количество каналов. На практике это означает способность распознавания '
                      'сложных иерархий признаков. Обычно после прохождения нескольких слоёв карта признаков '
                      'вырождается в вектор или даже скаляр, но таких карт признаков становятся сотни. На выходе '
                      'свёрточных слоёв сети дополнительно устанавливают несколько слоёв полносвязной нейронной '
                      'сети (перцептрон), на вход которому подаются оконечные карты признаков.',
            arch_img=b64img,
            arch_img_desc='Архитектура модели',
            history=None,
            history_img='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xOTJkznuuOO45557AFi3bh0zZ85k6tSpTJ48md///vek02nmzp3b0feHP/xhxNUXrpALmT8TTv7MzB4HBrv7suKWJSISH//88GssX7utqNucNHYwXzvr2Jz6PvDAAyxZsoSlS5eyYcMGTjzxRGbOnMmdd97JRz/6Ua6//nrS6TS7du1iyZIlrFmzhldffRWALVu2FLXuUipkKKkFZvbfzazW3d9WeImIROu5557joosuIplMMmrUKD74wQ/ywgsvcOKJJ3LLLbfw9a9/nVdeeYVBgwZx2GGHsWrVKq655hoef/xxBg8eHHX5BSvkNPrvAxcA3zKzF4C7gUfcXVfziUi/lOueUqnNnDmThQsX8utf/5q5c+fyhS98gUsuuYSlS5fyxBNP8LOf/Yx7772Xm2++OepSC5L3Hpi7/y48jHgY8HPgEwQncoiISAQ+8IEPcM8995BOp2lqamLhwoWcdNJJrF69mlGjRnHFFVdw+eWX89JLL7FhwwYymQznnXceN9xwAy+9FMkogEVR6IXMNcBZBHti04HbilmUiIjkbvbs2SxatIgpU6ZgZnznO99h9OjR3HbbbXz3u9+loqKCgQMHcvvtt7NmzRrmzZtHJpMB4Fvf+lbE1Rcu58F8O1Ywuxc4CXgcuAf4XXhafSQ0mK+IRGHFihUcc8wxUZcRa939DPtqMN92vwAucvd0AeuKiIgURSGn0T/RF4WIiIjko5ALmUVERCKnABMRkVgq5ELm2WY2JGt+qJmdW9SqRERE9qOQPbCvufvW9hl33wJ8rWgViYiI5KCQAOtunYKuJxMRESlUoaPR/8DMDg8fPyAYlV5ERA5CbW1tUZfQrUIC7BqgheAi5nuAPcBni1mUiIjk5txzz+WEE07g2GOPZf78+QA8/vjjTJ8+nSlTpvChD30IgB07djBv3jyOO+44jj/+eO6//36g800x77vvPubOnQvA3Llzueqqq3jve9/Ltddey5/+9Cfe9773MW3aNE455RTeeOMNANLpNH//93/P5MmTOf744/nJT37Cs88+y7nnntux3aeeeorZs2cX/b0Xch3YTuC6olciIhJXj10H618p7jZHHwdnfHu/3W6++WaGDx/O7t27OfHEEznnnHO44oorWLhwIRMmTGDTpk0AfPOb32TIkCG88kpQ5+bNm/e77cbGRv7whz+QTCbZtm0bv//9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',
            history_params={'verbose': 1, 'epochs': 15, 'steps': 469},
            metrics={
                'loss': 0.002,
                'accuracy': 99.9829
            },
            # metrics_colors={
            #     'loss': 'success',
            #     'accuracy': 'warning',
            # }
        )))


# @app.route('/results')
# def results():
#     return render_template('results.html', comments=dataclasses.asdict(simple_comment))


if __name__ == '__main__':
    app.run()
