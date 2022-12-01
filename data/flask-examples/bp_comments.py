from datetime import datetime

import flask
from flask import Blueprint, jsonify, request, abort

from .util import state, url_for, get_post_or_404, get_comment_or_404, jsonify_comment

mod = Blueprint('comments', __name__)

@mod.route('/article/<post_id>/comments')
def get_comments(post_id):
    post = get_post_or_404(post_id)
    comment_links = [
        url_for('.get_comment', post_id=post_id, comment_id=i) 
        for i, comment in enumerate(post['comments'])
    ]
    return jsonify(
        _links={'self': url_for('.get_comments', id=post_id)},
        data=[dict(_links=dict(self=link)) for link in comment_links])

@mod.route('/article/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    post = get_post_or_404(post_id)
    comment_id = len(post['comments'])
    comment = {
        'postedDate': datetime.utcnow(),
        'author_id': request.authorization.username,
        **request.json,
    }
    post['comments'].append(comment)
    result = jsonify_comment(post_id, comment_id, comment)
    result.headers['Location'] = url_for('.get_comment', post_id=post_id, comment_id=comment_id)
    return result, 201

@mod.route('/article/<post_id>/comments/<int:comment_id>')
def get_comment(post_id, comment_id):
    comment = get_comment_or_404(post_id, comment_id)
    return jsonify_comment(post_id, comment_id, comment)
    
@mod.route('/article/<post_id>/comments/<int:comment_id>', methods=['PUT'])
def update_comment(post_id, comment_id):
    comment = get_comment_or_404(post_id, comment_id)
    comment.update({
        'postedDate': datetime.utcnow(),
        'author_id': request.authorization.username,
        **request.json,
    })
    return jsonify_comment(post_id, comment_id, comment)

@mod.route('/article/<post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    post = get_post_or_404(post_id)
    if len(post[comments]) <= comment_id:
        abort(404)
    del post['comments'][comment_id]
    return '', 204
