from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    evaluations = db.relationship("Evaluation", backref='user', lazy=True)

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, unique=False)
    ref_pmid = db.Column(db.Integer, unique=False)
    eval_pmid = db.Column(db.Integer, unique=False)
    eval_score = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False)