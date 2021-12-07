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

    with open('resnet50.png', 'rb') as f:
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
            metrics=[
                ('loss', str(0.002)),
                ('accuracy', str(99.9829))
            ]
        )))


# @app.route('/results')
# def results():
#     return render_template('results.html', comments=dataclasses.asdict(simple_comment))


if __name__ == '__main__':
    app.run()
