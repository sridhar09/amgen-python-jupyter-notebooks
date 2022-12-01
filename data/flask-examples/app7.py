from flask import Flask, jsonify, url_for

from . import app7_posts
from .app7_util import url_for

app = Flask(__name__)

app.register_blueprint(app7_posts.mod, url_prefix='/api')

@app.route('/')
def get_root():
    return jsonify(_links={'posts': url_for('posts.get_articles')})
