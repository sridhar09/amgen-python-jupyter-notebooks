import flask

state = {'posts': {}}

def url_for(*args, **kwargs):
    return flask.url_for(*args, _external=True, **kwargs)
