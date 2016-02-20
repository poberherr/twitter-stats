from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD


class Followers(db.Model, CRUD):
    __tablename__ = 'followers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    twitter_id = db.Column(db.BigInteger)
    twitter_follower_id = db.Column(db.BigInteger)
    user_relation = db.relationship('Users', backref="users")

    def __init__(self, user_id, twitter_id, follower_id):
        self.user_id = user_id
        self.twitter_id = twitter_id
        self.twitter_follower_id = follower_id


# TODO: Unused right now - either adapt or delete - comment in views.
class FollowerSchema(Schema):

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    twitter_id = fields.Integer()
    twitter_follower_id = fields.Integer()

    class Meta:
        type_ = 'followers'
