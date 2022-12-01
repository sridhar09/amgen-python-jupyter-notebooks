import hmac

import flask
from flask import jsonify, request, abort

state = {
    'posts': {},
    'authors': {
        'rick': {
            'fullName': 'Rick Copeland',
            'password': 'seekrit',
        }
    },
}

def verify_password():
    if not request.authorization:
        abort(401)
    author = state['authors'].get(request.authorization.username)
    if author is None:
        abort(403)
    good_password = hmac.compare_digest(
        author['password'], request.authorization.password
    )
    # Please note that the approach below is *insecure* 
    #   -- you should use hashing like bcrypt or scrypt to store passwords, 
    #   and you should use a digest comparison
    # good_password = (author['password'] == request.authorization.password)
    if not good_password:
        abort(403)
    

def url_for(*args, **kwargs):
    return flask.url_for(*args, _external=True, **kwargs)

def get_author_or_404(author_id):
    author = state['authors'].get(author_id)
    if not author:
        abort(404)
    return author
    
def get_post_or_404(post_id):
    post = state['posts'].get(post_id)
    if not post:
        abort(404)
    return post
    
def get_comment_or_404(post_id, comment_id):
    post = get_post_or_404(post_id)
    comment = post['comments'][comment_id]
    return comment
    
def jsonify_post(post_id, post, **kwargs):
    return jsonify(
        _links={
            'self': url_for('posts.get_post', post_id=post_id),
            'comments': url_for('comments.get_comments', post_id=post_id),
            'author': url_for('authors.get_author', author_id=post['author_id']),
        },
        postedDate=post['postedDate'].isoformat(),
        title=post['title'],
        body=post['body']
    )

def jsonify_comment(post_id, comment_id, comment):
    return jsonify(
        _links={
            'self': url_for('comments.get_comment', post_id=post_id, comment_id=comment_id),
            'post': url_for('posts.get_post', post_id=post_id),
            'author': url_for('authors.get_author', author_id=comment['author_id']),
        },
        body=comment['body'],
    )

def jsonify_author(author_id, author):
    return jsonify(
        _links={'self': url_for('authors.get_author', author_id=author_id)},
        fullName=author['fullName'],
    )
