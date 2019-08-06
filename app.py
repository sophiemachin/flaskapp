from flask import Flask, request
import string
from collections import Counter
import flask
from flask_cors import cross_origin, CORS
import ast

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/route1')
def route1():
    return 'This is route1'


def count_words(s, capitals):
    punc_to_remove = string.punctuation.translate({
        ord('-'): None,
    })

    s = " ".join(s.split())

    s = s.replace('\n', ' ')
    no_punc = s.translate(str.maketrans('', '', punc_to_remove))
    print(capitals)
    if capitals == 'lower':
        s = no_punc.lower()
    return Counter(s.split())


@app.route('/json', methods=['GET', 'POST'])
@cross_origin(origin='*')
def json():

    d = ast.literal_eval(request.data.decode('utf-8'))
    s = d['data']
    capitals = d['capitals']

    count = dict(count_words(s, capitals))
    return flask.jsonify(count), 200


if __name__ == '__main__':
    app.run()
