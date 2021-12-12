from collections import namedtuple
from random import randint

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from mongoengine import connect

from report import Report, Model
from res.test_data import simple_comment, simple_report, toxic_model

app = Flask(__name__)
bootstrap = Bootstrap(app)
connect('nyadb')
Group = namedtuple('Group', 'header name hint models')


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
    return render_template(
        'predict.html',
        groups=(
            Group(
                header='Токсичность',
                name='toxic',
                hint='Проводить анализ токсичности',
                models=Model.objects(target='toxic')
            ),
            Group(
                header='Саркастичность',
                name='sarcasm',
                hint='Проводить анализ саркастичности',
                models=Model.objects(target='sarcasm')
            ),
            Group(
                header='Тональность',
                name='sentiment',
                hint='Проводить анализ тональности',
                models=Model.objects(target='sentiment')
            ),
        ),
    )


@app.route('/results')
def results():
    return render_template(
        'results.html',
        comments=make_prediction(simple_comment)
    )


@app.route('/reports')
def reports():
    return render_template(
        'reports.html',
        reports=Report.objects
    )


@app.route('/report/<string:title>')
def report(title):
    return render_template(
        'model_report.html',
        **Report.objects.get(title=title).to_dict()
    )


if __name__ == '__main__':
    app.run()
