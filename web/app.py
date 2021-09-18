from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from mako.template import Template
from model import ToxicModel


app = Flask(__name__)
bootstrap = Bootstrap(app)
toxic_model = ToxicModel()
template = Template(filename='templates/base.html')


@app.route('/predict/<int:x>')
def hello_world(x):
    return template.render(x=toxic_model.predict(x))


if __name__ == '__main__':
    app.run()
