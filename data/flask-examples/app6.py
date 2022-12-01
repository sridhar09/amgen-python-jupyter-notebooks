from datetime import datetime
from uuid import uuid4

import flask
from flask import Flask, jsonify, request, abort


app = Flask(__name__)

state = {
    'articles': { }
#         uuid4().hex: {
#             'postedDate': datetime.utcnow(),
#             'authorName': 'rick',
#             'title': 'first!',
#             'body': 'First post!'
#         }
#     }
}

def url_for(*args, **kwargs):
    return flask.url_for(*args, _external=True, **kwargs)

@app.route('/')
def get_root():
    return jsonify(_links={'articles': url_for('get_articles')})

@app.route('/article')
def get_articles():
    links = [url_for('get_article', id=id) for id in state['articles']]
    return jsonify(
        _links={'self': url_for('get_articles')},
        data=[dict(_links=dict(self=link)) for link in links])

@app.route('/article', methods=['POST'])
def create_article():
    _id = uuid4().hex
    article = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        'request_args': request.args,
        **request.json   # json.loads(request.text)
    }
    # if you don't like the **syntax, you can also article.update(request.json)
    state['articles'][_id] = article
    result = jsonify_article(_id, article)
    result.headers['Location'] = url_for('get_article', id=_id)
    return result, 201

@app.route('/article/<id>')
def get_article(id):
    article = state['articles'].get(id)
    if not article:
        abort(404)
    return jsonify_article(id, article)

@app.route('/article/<id>', methods=['PUT'])
def update_article(id):
    article = state['articles'].get(id)
    if not article:
        abort(404)
    article = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json  # python 3.5?6?
    }
    # post.update(request.json)
    state['articles'][id] = article
    return jsonify_article(id, article)

@app.route('/article/<id>', methods=['DELETE'])
def delete_article(id):
    state['articles'].pop(id, None)
    return '', 204

def jsonify_article(id, article, **kwargs):
    return jsonify(
        _links={'self': url_for('get_article', id=id)},
        postedDate=article['postedDate'].isoformat(),
        authorName=article['authorName'],
        title=article['title'],
        body=article['body'],
        request_args=article.get('request_args', None)
    )
    
