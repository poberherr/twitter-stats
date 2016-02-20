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
    from app.users.views import users
    app.register_blueprint(users, url_prefix='/users')

    from app.followers.views import followers
    app.register_blueprint(followers, url_prefix='/followers')

    # Twitter fetch module
    # TODO: Move twitter module


    return app
