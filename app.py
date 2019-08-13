from flask import Flask, request
import string
from collections import Counter
import flask
from flask_cors import cross_origin, CORS
import ast
from werkzeug.utils import secure_filename
import os
import glob

app = Flask(__name__)
CORS(app)

FILE = ''

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello, World!'


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


@app.route('/analyse', methods=['GET', 'POST'])
@cross_origin(origin='*')
def analyse():
    """Run the analysis

    If d['file'] == file, analyses the files in uploads
    Else analyses the text in d['data']

    """

    counter = Counter()

    d = ast.literal_eval(request.data.decode('utf-8'))

    f = d['file'] == 'file'

    c = d['capitals'] == 'lower'
    p = d['punctuation'] == 'remove'
    u = d['uploaded']

    if f:
        for file in glob.glob(os.getcwd() + "/uploads/*.txt"):
            name = file.rsplit('/', 1)[1]
            if name in u:
                with open(file, 'rb') as f:
                    data = f.readlines()
                    for line in data:
                        s = line.decode('utf-8')
                        counter += count_words(s, c, p)
    else:
        s = d['data']
        counter += count_words(s, c, p)

    return flask.jsonify(dict(counter)), 200


@app.route('/upload', methods=['GET', 'POST'])
@cross_origin(origin='*')
def upload():
    """Upload files to the uploads directory"""

    uploads = os.getcwd() + '/uploads'
    uploaded = []

    for fn in request.files:
        file = request.files[fn]
        if '/' in file.filename:
            name = file.filename.rsplit('/', 1)[1]
        else:
            name = file.filename
        filename = secure_filename(name)
        uploaded.append(filename)
        file.save(os.path.join(uploads, filename))
    return flask.jsonify(uploaded), 200

@app.route('/remove', methods=['GET', 'POST'])
@cross_origin(origin='*')
def remove():
    """Remove all uploads"""

    for f in glob.glob(os.getcwd() + "/uploads/*.txt"):
        os.remove(f)

    return 'ok', 200


if __name__ == '__main__':
    app.run()

