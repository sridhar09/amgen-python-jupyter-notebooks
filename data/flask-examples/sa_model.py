from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postedDate = db.Column(db.DateTime)
    authorName = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    postedDate = db.Column(db.DateTime)
    authorName = db.Column(db.String)
    content = db.Column(db.String)
    
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
