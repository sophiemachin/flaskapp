from flask import Flask, request
import string
from collections import Counter
import flask
from flask_cors import cross_origin, CORS
import ast
import nltk

app = Flask(__name__)
CORS(app)

PARTS = [
    'CC',
    'JJ',
    'IN',
    'NN',
    'PRP',
    'RB',
    'VB',
    'VBD',
]


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


def count_words(s, remove_capitals, remove_punc):
    """Count occurrences of words in a  string

    Words are separated by a space

    Removes all punctuation except hyphens

    Optionally converts all charts to lower case

    s                   - string, to count word occurrences
    remove_capitals     - bool, if True remove capitals (convert to lowercase)
    remove_punc         - bool, if True remove punctuation

    """

    s = " ".join(s.split())
    if remove_punc:
        punc_to_remove = get_punc_to_remove()
        s = remove_punctuation(s, punc_to_remove)

    if remove_capitals:
        s = s.lower()

    return Counter(s.split())

def year_3_analysis(s):

    tokens = nltk.word_tokenize(s)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)

    l = []

    for entity in entities:
        if entity[1][:2] in PARTS:
            l.append((entity[0], entity[1][:2]))
        else:
            l.append((entity[0], None))

    return l


@app.route('/analyse', methods=['GET', 'POST'])
@cross_origin(origin='*')
def analyse():
    """Run the analysis

    Analyses the text in d['data']

    """

    d = ast.literal_eval(request.data.decode('utf-8'))

    s = d['data']

    analysis = year_3_analysis(s)

    return flask.jsonify(analysis), 200



if __name__ == '__main__':
    app.run()

