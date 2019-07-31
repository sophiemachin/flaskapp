from flask import Flask, request
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


@app.route('/json', methods=['GET', 'POST'])
@cross_origin(origin='*')
def json():
    print(request.data)
    data = {'somekey': 'somevalue'}
    return flask.jsonify(data), 200


if __name__ == '__main__':
    app.run()
