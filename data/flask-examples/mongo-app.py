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
    res = mongo.db.post.insert_one(post)
    _id = res.inserted_id
    post['_id'] = _id
    result = jsonify_post(post)
    result.headers['Location'] = url_for('get_post', post_id=post['_id'], _external=True)
    return result

@app.route('/post/<ObjectId:post_id>')
def get_post(post_id):
    post = mongo.db.post.find_one_or_404({'_id': post_id})
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

def jsonify_post(post):
    return jsonify(
        _links={'self': url_for('get_post', post_id=post['_id'], _external=True)},
        postedDate=post['postedDate'].isoformat(),
        authorName=post['authorName'],
        title=post['title'],
        content=post['content'],
    )
