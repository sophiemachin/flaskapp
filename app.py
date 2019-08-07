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

def get_punc_to_remove():
    """Returns a string

    Ensures that '-' (a dash) is not in the string

    """

    return string.punctuation.translate({
        ord('-'): None,
    })

def remove_punctuation(s, punc_to_remove):
    """Remove chars from a string

    s               - string, to remove chars from
    punc_to_remove  - string, chars to remove

    """

    return s.translate(str.maketrans('', '', punc_to_remove))


def count_words(s, capitals):
    punc_to_remove = get_punc_to_remove()

    s = " ".join(s.split())

    s = remove_punctuation(s, punc_to_remove)

    if not capitals:
        s = s.lower()
    return Counter(s.split())


@app.route('/json', methods=['GET', 'POST'])
@cross_origin(origin='*')
def json():

    d = ast.literal_eval(request.data.decode('utf-8'))
    s = d['data']
    c = d['capitals'] != 'lower'

    count = dict(count_words(s, c))
    return flask.jsonify(count), 200


if __name__ == '__main__':
    app.run()
