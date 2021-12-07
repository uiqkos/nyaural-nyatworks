import dataclasses

from flask import Flask
from flask import render_template, render_template_string
from flask_bootstrap import Bootstrap
from ml import *
from comment import Comment
from random import randint

from report import Report

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

example_report = Report(
    name='Heavy CNN',
    description='Heavy CNN with 10 hidden_layers',
    scores={
        'loss': '0.02',
        'accuracy': '98.981'
    }
)


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
    return render_template(
        'model_report.html',
        model=dict(
            name='Heavy CNN',
            description='Heavy CNN with 10 hidden_layers',
            scores=[
                dict(loss='0.02'),
                dict(accuracy='98.981'),
            ]
        )
    )

# @app.route('/results')
# def results():
#     return render_template('results.html', comments=dataclasses.asdict(simple_comment))


if __name__ == '__main__':
    app.run()
