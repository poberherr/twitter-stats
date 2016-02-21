from marshmallow_jsonapi import Schema, fields
from app.basemodels import db, CRUD


class Tweets(db.Model, CRUD):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.BigInteger, unique=True)
    created_at = db.Column(db.TIMESTAMP)
    text = db.Column(db.String(250))
    source = db.Column(db.String(250))
    in_reply_to_status_id = db.Column(db.BigInteger)
    in_reply_to_user_id = db.Column(db.BigInteger)
    in_reply_to_screen_name = db.Column(db.String(250))
    is_quote_status = db.Column(db.Boolean)
    retweet_count = db.Column(db.Integer)
    favorite_count = db.Column(db.Integer)

    def __init__(self, tweet_data, user_id):
        self.user_id = user_id
        self.tweet_id = tweet_data.id # the only 'interesting' line
        self.created_at = tweet_data.created_at
        self.text = tweet_data.text
        self.source = tweet_data.source
        self.in_reply_to_status_id = tweet_data.in_reply_to_status_id
        self.in_reply_to_user_id = tweet_data.in_reply_to_user_id
        self.in_reply_to_screen_name = tweet_data.in_reply_to_screen_name
        self.is_quote_status = tweet_data.is_quote_status
        self.retweet_count = tweet_data.retweet_count
        self.favorite_count = tweet_data.favorite_count
        self.user_id = user_id

class TweetsSchema(Schema):
    # add user_id to schema and return
    id = fields.Integer(dump_only=True)
    tweet_id = fields.Integer()
    created_at = fields.String()
    text = fields.String()
    source = fields.String()
    in_reply_to_status_id = fields.Integer()
    in_reply_to_user_id = fields.Integer()
    in_reply_to_screen_name = fields.String()
    is_quote_status = fields.Boolean()
    retweet_count = fields.Integer()
    favorite_count = fields.Integer()


    class Meta:
        type_ = 'tweets'
