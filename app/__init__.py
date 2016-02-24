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

    from app.statistics.views import statistics
    app.register_blueprint(statistics, url_prefix='/statistics')

    from app.tweets.views import tweets
    app.register_blueprint(tweets, url_prefix='/tweets')

    from app.users.views import users
    app.register_blueprint(users, url_prefix='/users')

    return app
