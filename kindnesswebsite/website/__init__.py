from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdlgjfaiowejklvmd4%$%^DFSFD8979iJGHNDS5wgfb&^*HGHDt67dHSRTEGZHSftyretz' ## secret key

    # register views
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/") # prefix for the view
    app.register_blueprint(auth, url_prefix="/")

    return app

