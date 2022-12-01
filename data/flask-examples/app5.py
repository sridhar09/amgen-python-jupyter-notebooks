from datetime import datetime
from uuid import uuid4

import flask
from flask import Flask, jsonify, request, abort


app = Flask(__name__)

state = {
    'articles': {
        uuid4().hex: {
            'postedDate': datetime.utcnow(),
            'authorName': 'rick',
            'title': 'first!',
            'body': 'First post!'
        }
    }
}

def url_for(*args, **kwargs):
    return flask.url_for(*args, _external=True, **kwargs)

# /post/123 - *not* _external=True
# http://localhost:5000/post/123 - _external=True


@app.route('/')
def get_root():
    return jsonify(_links={
        'self': url_for('get_root'),
        'articles': url_for('get_articles')
    })

@app.route('/article')
def get_articles():
    article_links = [
        url_for('get_article', id=id) 
        for id in state['articles']
    ]
    return jsonify(
        _links={'self': url_for('get_articles')},
        data=[
            dict(_links=dict(self=link)) 
            for link in article_links
        ]
    )

@app.route('/article/<id>')
def get_article(id):
    # post = state['articles'][id]  # could generate a KeyError => 500 Error
    article = state['articles'].get(id)
    if article is None:
        abort(404)
    return jsonify(
        _links={'self': url_for('get_article', id=id)},
        postedDate=article['postedDate'].isoformat(),
        authorName=article['authorName'],
        title=article['title'],
        body=article['body']
    )
