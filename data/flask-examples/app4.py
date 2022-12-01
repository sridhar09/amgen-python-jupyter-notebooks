import flask

app = flask.Flask(__name__)

@app.route('/profile/<username>')
def get_profile(username):
    return flask.jsonify(username=username)

@app.route('/userinfo')
def get_userinfo():
    username = flask.request.authorization['username']
    profile_url = flask.url_for(
        'get_profile', username=username, 
        _external=True
    )
    return flask.jsonify(
        _links={'profile': profile_url},
        username=username,
        # don't do this in production, obviously
        password=flask.request.authorization['password'] ,
        headers=dict(flask.request.headers)
    )
