from datetime import datetime

from flask import Flask, url_for, jsonify, request, abort

from .sa_model import db, Post, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# db = SQLAlchemy(app)


@app.route('/')
def get_root():
    return jsonify(_links={'posts': url_for('get_posts', _external=True)})


@app.route('/post')
def get_posts():
    post_links = [
        url_for('get_post', post_id=post.id, _external=True) 
        for post in Post.query]
    return jsonify(
        _links={'self': url_for('get_posts', _external=True)},
        posts=[dict(_links=dict(self=link)) for link in post_links])

@app.route('/post', methods=['POST'])
def create_post():
    post = Post(
        authorName=request.authorization.username,
        postedDate=datetime.utcnow(),
        title=request.json['title'],
        content=request.json['content'],
    )
    db.session.add(post)
    db.session.commit()
    result = jsonify_post(post)
    result.headers['Location'] = url_for('get_post', post_id=post.id, _external=True)
    return result, 201

@app.route('/post/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return jsonify_post(post)

@app.route('/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    post.authorName = request.authorization.username
    post.postedDate = datetime.utcnow()
    post.title = request.json['title']
    post.content = request.json['content']
    db.session.commit()
    return jsonify_post(post)

@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return '', 204

def jsonify_post(post):
    return jsonify(
        _links={'self': url_for('get_post', post_id=post.id, _external=True)},
        postedDate=post.postedDate.isoformat(),
        authorName=post.authorName,
        title=post.title,
        content=post.content,
    )
