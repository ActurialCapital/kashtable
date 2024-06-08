import os
import os.path as op

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Configuration class for the Flask application.

    Attributes
    ----------
    SECRET_KEY : str
        Secret key used for securely signing session cookies.

    DATABASE_FILE : str
        Name of the SQLite database file.

    SQLALCHEMY_DATABASE_URI : str
        Database URI for SQLAlchemy to connect to the database.

    SQLALCHEMY_ECHO : bool
        Controls the verbosity of SQLAlchemy logging.

    SQLALCHEMY_TRACK_MODIFICATIONS : bool
        Tracks modifications of objects and emits signals.

    MAIL_SERVER : str
        SMTP server for sending emails.

    MAIL_PORT : int
        Port number for the SMTP server.

    MAIL_USE_TLS : bool
        Specifies whether to use TLS for email communication.

    MAIL_USERNAME : str
        Username for accessing the SMTP server.

    MAIL_PASSWORD : str
        Password for accessing the SMTP server.

    FLASK_ADMIN_BOOTSTRAP : str
        Bootstrap version for Flask-Admin templates.

    FLASK_ADMIN_SWATCH : str
        Bootstrap theme for Flask-Admin templates.

    FILE_PATH : str
        Path to the directory for storing files.

    BASIC_AUTH_USERNAME : str
        Username for basic authentication.

    BASIC_AUTH_PASSWORD : str
        Password for basic authentication.
    """
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_FILE = 'db.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    FLASK_ADMIN_BOOTSTRAP = 'bootstrap3'
    FLASK_ADMIN_SWATCH = 'Slate'  # https://bootswatch.com/

    FILE_PATH = op.join(op.dirname(__file__), 'files')

    BASIC_AUTH_USERNAME = 'alfie@example.com'
    BASIC_AUTH_PASSWORD = 'alfiephillips'
