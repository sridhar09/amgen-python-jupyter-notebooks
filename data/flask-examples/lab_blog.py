from flask import Flask, jsonify, url_for

from . import bp_posts
from . import bp_comments
from . import bp_authors
from .util import url_for

app = Flask(__name__)

app.register_blueprint(bp_posts.mod, url_prefix='/api')
app.register_blueprint(bp_comments.mod, url_prefix='/api')
app.register_blueprint(bp_authors.mod, url_prefix='/api')

@app.route('/')
def get_root():
    return jsonify(_links={
        'posts': url_for('posts.get_posts'),
    })
