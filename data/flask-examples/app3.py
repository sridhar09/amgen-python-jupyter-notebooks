import flask

app = flask.Flask(__name__)

state = {'name': 'world'}

@app.route('/')
def get_root():
    return flask.jsonify(hello=state['name'])

@app.route('/', methods=['PUT'])
def set_name():
    body = flask.request.json  # resolves to None if no valid JSON Content-Type header
    state['name'] = body['name']
    return flask.jsonify(name=state['name'])
