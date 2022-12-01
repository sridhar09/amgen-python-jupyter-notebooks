from datetime import datetime

from flask import Flask, url_for, jsonify, request, abort

from mongo_model import mongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://class:classword@training.i7auh.mongodb.net/class'
mongo.init_app(app)


@app.route('/')
def get_root():
    return jsonify(_links={'posts': url_for('get_posts', _external=True)})


@app.route('/post')
def get_posts():
    post_links = [
        url_for('get_post', post_id=post['_id'], _external=True) 
        for post in mongo.db.post.find()]
    return jsonify(
        _links={'self': url_for('get_posts', _external=True)},
        posts=[dict(_links=dict(self=link)) for link in post_links])

@app.route('/post', methods=['POST'])
def create_post():
    post = dict(
        authorName=request.authorization.username,
        postedDate=datetime.utcnow(),
        title=request.json['title'],
        content=request.json['content'],
    )
    _id = mongo.db.post.insert_one(post).inserted_id
    post['_id'] = _id
    result = jsonify_post(post)
    result.headers['Location'] = url_for('get_post', post_id=post['_id'], _external=True)
    return result

@app.route('/post/<ObjectId:post_id>')
def get_post(post_id):
    post = mongo.db.post.find_one_or_404({'_id': post_id})
    if not post:
        abort(404)
    return jsonify_post(post)

@app.route('/post/<ObjectId:post_id>', methods=['PUT'])
def update_post(post_id):
    post = mongo.db.post.find_one_or_404({'_id': post_id})
    post.update(
        authorName=request.authorization.username,
        postedDate=datetime.utcnow(),
        title=request.json['title'],
        content=request.json['content']
    )
    db.post.replace_one({'_id': post_id}, post)
    return jsonify_post(post)

@app.route('/post/<ObjectId:post_id>', methods=['DELETE'])
def delete_post(post_id):
    mongo.db.post.delete_one({'_id': post_id})
    return '', 204


@app.route('/post/<ObjectId:post_id>/comment')
def get_comments(post_id):
    post = mongo.db.post.find_one_or_404({'_id': post_id})
    comment_links = [
        url_for('get_comment', post_id=post_id, comment_id=cid, _external=True) 
        for cid, c in enumerate(post.get('comments', []))
    ]
    return jsonify(
        _links={'self': url_for('get_comments', post_id=post_id, _external=True)},
        comments=[dict(_links=dict(self=link)) for link in comment_links])

@app.route('/post/<ObjectId:post_id>/comment', methods=['POST'])
def create_comment(post_id):
    post = mongo.db.post.find_one_or_404({'_id': post_id})
    comment = dict(
        authorName=request.authorization.username,
        postedDate=datetime.utcnow(),
        content=request.json['content'],
    )
    cid = len(post.get('comments', []))
    post.setdefault('comments', []).append(comment)
    mongo.db.post.replace_one({'_id': post['_id']}, post)
    result = jsonify_comment(post_id, cid, comment)
    result.headers['Location'] = url_for('get_comment', post_id=post_id, comment_id=cid, _external=True)
    return result, 201

@app.route('/post/<ObjectId:post_id>/comment/<int:comment_id>')
def get_comment(post_id, comment_id):
    post, comment = get_comment_or_404(post_id, comment_id)
    return jsonify_comment(post_id, comment_id, comment)
    
@app.route('/post/<int:post_id>/comment/<int:comment_id>', methods=['PUT'])
def update_comment(post_id, comment_id):
    post, comment = get_comment_or_404(post_id, comment_id)
    comment.update(
        postedDate=datetime.utcnow(),
        authorName=request.authorization.username,
        content=request.json['content'],
    )
    mongo.db.post.replace_one({'_id': post['_id']}, post)    
    return jsonify_comment(post_id, comment_id, comment)

@app.route('/post/<int:post_id>/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    post, comment = get_comment_or_404(post_id, comment_id)
    del post[comment_id]
    mongo.db.post.replace_one({'_id': post['_id']}, post)    
    return '', 204

def get_comment_or_404(post_id, comment_id):
    post = mongo.db.post.find_one_or_404(post_id)
    if len(post['comments']) <= comment_id:
        abort(404)
    return post, post['comments'][comment_id]

def jsonify_post(post):
    return jsonify(
        _links={
            'self': url_for('get_post', post_id=post['_id'], _external=True),
            'comments': url_for('get_comments', post_id=post['_id'], _external=True)
        },
        postedDate=post['postedDate'].isoformat(),
        authorName=post['authorName'],
        title=post['title'],
        content=post['content'],
    )

def jsonify_comment(post_id, comment_id, comment):
    return jsonify(
        _links={
            'self': url_for('get_comment', post_id=post_id, comment_id=comment_id, _external=True),
            'post': url_for('get_post', post_id=post_id, _external=True),
        },
        postedDate=comment['postedDate'].isoformat(),
        authorName=comment['authorName'],
        content=comment['content'],
    )

