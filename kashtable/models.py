from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from sqlalchemy_utils import ChoiceType, EmailType
from kashtable import db, login_manager

AVAILABLE_USER_TYPES = [
    (u'admin', u'Admin'),
    (u'client', u'Client'),
]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Represents a user in the system.

    Attributes
    ----------
    id : int
        The unique identifier for the user.
    type : str
        The type of the user, defaults to 'client'.
    sqla_utils_choice_field : ChoiceType
        A choice field with available user types.
    company_name : str
        The name of the company associated with the user.
    street : str
        The street address of the user.
    postcode : str
        The postcode of the user's location.
    city : str
        The city of the user's location.
    country : str
        The country of the user's location.
    siren : str
        The SIREN number of the company associated with the user.
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    email : str
        The email address of the user.
    phone_number : str
        The phone number of the user.
    image_file : str
        The filename of the user's profile image.
    bundle : int
        The bundle associated with the user.
    activated : bool
        Indicates whether the user account is activated.
    password : str
        The hashed password of the user.
    file : relationship
        Relationship to the files uploaded by the user.

    Methods
    -------
    get_reset_token(expires_sec=1800)
        Generates a token for resetting the user's password.
    verify_reset_token(token)
        Verifies the reset token and returns the associated user.
    __str__()
        Returns a string representation of the user.
    __repr__()
        Returns a printable representation of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    # use a regular string field, for which we can specify a list of available choices later on
    type = db.Column(db.String(100), nullable=True, default='client')
    sqla_utils_choice_field = db.Column(ChoiceType(AVAILABLE_USER_TYPES), nullable=True)
    company_name = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(128), nullable=False)
    postcode = db.Column(db.String(7), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    siren = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='blank.jpg')
    bundle = db.Column(db.Integer, nullable=False)
    activated = db.Column(db.Boolean, nullable=False, default=True)
    password = db.Column(db.String(60), nullable=False)
    file = db.relationship('File', backref='client', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        Generates a token for resetting the user's password.

        Parameters
        ----------
        expires_sec : int, optional
            Expiry time for the token in seconds, by default 1800

        Returns
        -------
        str
            The generated reset token.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Verifies the reset token and returns the associated user.

        Parameters
        ----------
        token : str
            The reset token to verify.

        Returns
        -------
        User or None
            The user associated with the token if valid, None otherwise.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __str__(self):
        return f"{self.company_name}, {self.email}"

    def __repr__(self):
        return "User('{self.user_id}', '{self.company_name}', '{self.email}')"


class File(db.Model):
    """
    Represents a file uploaded by a user.

    Attributes
    ----------
    id : int
        The unique identifier for the file.
    name : str
        The name of the file.
    doc : PickleType
        The content of the file.
    date : DateTime
        The date and time when the file was uploaded.
    user_id : int
        The ID of the user who uploaded the file.
    user : relationship
        Relationship to the user who uploaded the file.

    Methods
    -------
    __repr__()
        Returns a printable representation of the file.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    doc = db.Column(db.PickleType(), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys=[user_id], backref='files')

    def __repr__(self):
        return f"User('{self.user_id}', '{self.date}', '{self.doc}')"
