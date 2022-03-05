from models.db import db


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('ratings', lazy=False))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False,)
    subject = db.relationship('Subject')
    score = db.Column(db.Integer)
