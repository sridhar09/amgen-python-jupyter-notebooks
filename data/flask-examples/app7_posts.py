from datetime import datetime
from uuid import uuid4

import flask
from flask import Blueprint, jsonify, request, abort

from .app7_util import state, url_for

mod = Blueprint('posts', __name__)

@mod.route('/article')
def get_articles():
    post_links = [url_for('.get_article', id=id) for id in state['posts']]
    return jsonify(
        _links={
            'self': url_for('.get_articles'),
            'home': url_for('get_root'),
        },
        data=[dict(_links=dict(self=link)) for link in post_links])

@mod.route('/article', methods=['POST'])
def create_article():
    post_id = uuid4().hex
    post = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json
    }
    state['posts'][post_id] = post
    result = jsonify_article(post_id, post)
    result.headers['Location'] = url_for('.get_article', id=post_id)
    return result

@mod.route('/article/<id>')
def get_article(id):
    post = state['posts'].get(id)
    if not post:
        abort(404)
    return jsonify_article(id, post)

@mod.route('/article/<id>', methods=['PUT'])
def update_article(id):
    post = state['posts'].get(id)
    if not post:
        abort(404)
    post = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json
    }
    state['posts'][id] = post
    return jsonify_article(id, post)

@mod.route('/article/<id>', methods=['DELETE'])
def delete_article(id):
    state['posts'].pop(id)
    return '', 204

def jsonify_article(id, post, **kwargs):
    return jsonify(
        _links={'self': url_for('.get_article', id=id)},
        postedDate=post['postedDate'].isoformat(),
        authorName=post['authorName'],
        title=post['title'],
        body=post['body']
    )
