import flask

app = flask.Flask(__name__)

@app.route('/')
def get_root():
    return flask.jsonify(hello='world')

@app.route('/<name>')
def get_name(name):
    print(flask.request.args)
    return flask.jsonify(hello=name, args=flask.request.args)
