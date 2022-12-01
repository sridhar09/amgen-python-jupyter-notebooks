from datetime import datetime
from uuid import uuid4

import flask
from flask import Blueprint, jsonify, request, abort

from .util import state, url_for, get_post_or_404

mod = Blueprint('posts', __name__)

@mod.route('/article')
def get_posts():
    post_links = [url_for('.get_post', post_id=post_id) for post_id in state['posts']]
    return jsonify(
        _links={'self': url_for('.get_posts')},
        data=[dict(_links=dict(self=link)) for link in post_links])

@mod.route('/article', methods=['POST'])
def create_post():
    post_id = uuid4().hex
    post = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json,
        'comments': [],
    }
    state['posts'][post_id] = post
    result = jsonify_post(post_id, post)
    result.headers['Location'] = url_for('.get_post', post_id=post_id)
    return result, 201

@mod.route('/article/<post_id>')
def get_post(post_id):
    post = get_post_or_404(post_id)
    return jsonify_post(post_id, post)

@mod.route('/article/<post_id>', methods=['PUT'])
def update_post(post_id):
    post = get_post_or_404(post_id)
    post.update({
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json
    })
    return jsonify_post(id, post)

@mod.route('/article/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    state['posts'].pop(post_id)
    return '', 204

def jsonify_post(post_id, post, **kwargs):
    return jsonify(
        _links={
            'self': url_for('.get_post', post_id=post_id),
            'comments': url_for('comments.get_comments', post_id=post_id)
        },
        postedDate=post['postedDate'].isoformat(),
        authorName=post['authorName'],
        title=post['title'],
        body=post['body']
    )
