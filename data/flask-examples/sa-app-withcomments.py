from datetime import datetime

from flask import Flask, url_for, jsonify, request, abort

from .sa_model import db, Post, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


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
    return result

@app.route('/post/<int:post_id>')
def get_post(post_id):
    post = get_post_or_404(post_id)
    return jsonify_post(post)

@app.route('/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = get_post_or_404(post_id)
    post.authorName = request.authorization.username
    post.postedDate = datetime.utcnow()
    post.title = request.json['title']
    post.content = request.json['content']
    db.session.commit()
    return jsonify_post(post)

@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = get_post_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204

@app.route('/post/<int:post_id>/comment')
def get_comments(post_id):
    post = get_post_or_404(post_id)
    comment_links = [
        url_for('get_comment', post_id=post_id, comment_id=c.id, _external=True) 
        for c in post.comments
    ]
    return jsonify(
        _links={'self': url_for('get_comments', post_id=post_id, _external=True)},
        comments=[dict(_links=dict(self=link)) for link in comment_links])

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def create_comment(post_id):
    post = get_post_or_404(post_id)
    comment = Comment(
        authorName=request.authorization.username,
        postedDate=datetime.utcnow(),
        #post_id=post_id,
        content=request.json['content'],
    )
    post.comments.append(comment)
    #db.session.add(comment)
    db.session.commit()
    result = jsonify_comment(comment)
    result.headers['Location'] = url_for('get_comment', post_id=post_id, comment_id=comment.id, _external=True)
    return result, 201

@app.route('/post/<int:post_id>/comment/<int:comment_id>')
def get_comment(post_id, comment_id):
    comment = get_comment_or_404(post_id, comment_id)
    return jsonify_comment(comment)
    
@app.route('/post/<int:post_id>/comment/<int:comment_id>', methods=['PUT'])
def update_comment(post_id, comment_id):
    comment = get_comment_or_404(post_id, comment_id)
    comment.postedDate = datetime.utcnow()
    comment.authorName = request.authorization.username
    comment.content = request.json['content']
    db.session.commit()
    return jsonify_comment(comment)

@app.route('/post/<int:post_id>/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    comment = get_comment_or_404(post_id, comment_id)
    db.session.delete(comment)
    db.session.commit()
    return '', 204

def get_post_or_404(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return post
    
def get_comment_or_404(post_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        abort(404)
    if comment.post_id != post_id:
        abort(404)
    return comment

def jsonify_comment(comment):
    return jsonify(
        _links={
            'self': url_for('get_comment', post_id=comment.post_id, comment_id=comment.id, _external=True),
            'post': url_for('get_post', post_id=comment.post_id, _external=True),
        },
        postedDate=comment.postedDate.isoformat(),
        authorName=comment.authorName,
        content=comment.content,
    )

def jsonify_post(post):
    return jsonify(
        _links={
            'self': url_for('get_post', post_id=post.id, _external=True),
            'comments': url_for('get_comments', post_id=post.id, _external=True)
        },
        postedDate=post.postedDate.isoformat(),
        authorName=post.authorName,
        title=post.title,
        content=post.content,
    )
