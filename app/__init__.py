from flask import Flask, Response


class MyResponse(Response):
     default_mimetype = 'application/json'


# http://flask.pocoo.org/docs/0.10/patterns/appfactories/
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.response_class = MyResponse

    #Init Flask-SQLAlchemy
    from app.basemodels import db
    db.init_app(app)

    # Blueprints
    from app.followers.views import followers
    app.register_blueprint(followers, url_prefix='/followers')

    from app.tweet_statistics.views import tweet_statistics
    app.register_blueprint(tweet_statistics, url_prefix='/tweet_statistics')

    from app.tweets.views import tweets
    app.register_blueprint(tweets, url_prefix='/tweets')

    from app.fetch_network.views import fetch_network
    app.register_blueprint(fetch_network, url_prefix='/fetch_network')

    from app.users.views import users
    app.register_blueprint(users, url_prefix='/users')

    return app
