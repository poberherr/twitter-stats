from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD

class Users(db.Model, CRUD):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    twitter_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(250))
    screen_name = db.Column(db.String(250))
    location = db.Column(db.String(250))
    description = db.Column(db.String(250))
    url = db.Column(db.String(250))
    followers_count = db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    # ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
    created_at = db.Column(db.TIMESTAMP)
    favourites_count = db.Column(db.Integer)
    time_zone = db.Column(db.String(250))
    statuses_count = db.Column(db.Integer)
    modified_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, user_data):
        self.twitter_id = user_data.id
        self.name = user_data.name
        self.screen_name = user_data.screen_name
        self.location = user_data.location
        self.description = user_data.description
        self.url = user_data.url
        self.followers_count = user_data.followers_count
        self.friends_count = user_data.friends_count
        self.created_at = user_data.created_at
        self.favourites_count = user_data.favourites_count
        self.time_zone = user_data.time_zone
        self.statuses_count = user_data.statuses_count


# TODO: Be smarter and use : http://marshmallow-sqlalchemy.readthedocs.org/en/latest/recipes.html
class UsersSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    twitter_id = fields.Integer()
    name = fields.String()
    screen_name = fields.String()
    location = fields.String()
    description = fields.String()
    url = fields.String()
    followers_count = fields.Integer()
    friends_count = fields.Integer()
    # TODO: Handle time conversion since we want to sort in the DB
    created_at = fields.String()
    favourites_count = fields.Integer()
    time_zone = fields.String()
    statuses_count = fields.Integer()


     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}


    class Meta:
        type_ = 'users'
