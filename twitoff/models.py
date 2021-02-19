"""SQLalchemy models and utility functions for Twitoff App"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    """Twitter User Table that will correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True) #id column
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Tweet(DB.Model):

    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}".format(self.text)

def insert_example_users():
    john = User(id=1, name='John')
    ethan = User(id=2, name='Ethan')
    jimmy = User(id=3, name='Jimmy')
    DB.session.add(john)
    DB.session.add(ethan)
    DB.session.add(jimmy)
    DB.session.commit()