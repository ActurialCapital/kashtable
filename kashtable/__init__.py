from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_excel import init_excel
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_basicauth import BasicAuth
from flask_wtf.csrf import CSRFProtect

from kashtable.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
basic_auth = BasicAuth()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Parameters
    ----------
    config_class : Config, optional
        The configuration class for the Flask application, by default Config

    Returns
    -------
    Flask
        The configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # init app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    init_excel(app)
    admin = Admin(
        app, 
        name='BACKEND',
        template_mode=Config.FLASK_ADMIN_BOOTSTRAP
    )
    basic_auth.init_app(app)
    csrf.init_app(app)

    # admin
    from kashtable.models import User, File
    from kashtable.views import UserCRUD, FileCRUD  # MyView
    admin.add_view(UserCRUD(User, db.session))
    admin.add_view(FileCRUD(File, db.session))
    admin.add_link(MenuLink(name='App', url='/'))
    admin.add_link(MenuLink(name='Logout', url='/logout'))

    # routes
    from kashtable.users.routes import users
    from kashtable.main.routes import main
    from kashtable.posts.routes import posts
    from kashtable.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
