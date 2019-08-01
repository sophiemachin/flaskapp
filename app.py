from flask import Flask, request
import string
from collections import Counter
import flask
from flask_cors import cross_origin, CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/route1')
def route1():
    return 'This is route1'


def count_words(s):
    punc_to_remove = string.punctuation.translate({ord('-'): None})
    no_punc = s.translate(str.maketrans('', '', punc_to_remove))
    lower = no_punc.lower()
    return Counter(lower.split())


@app.route('/json', methods=['GET', 'POST'])
@cross_origin(origin='*')
def json():
    s = request.data.decode('utf-8')
    count = dict(count_words(s))
    return flask.jsonify(count), 200


if __name__ == '__main__':
    app.run()
