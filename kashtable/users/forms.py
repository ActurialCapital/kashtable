from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from wtforms import (
    StringField, 
    PasswordField, 
    SubmitField, 
    BooleanField,
    RadioField,
    TextAreaField,
    SelectField
    )
from kashtable.models import User


class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    This form allows users to register by providing their personal and company details.

    Attributes
    ----------
    first_name : StringField
        Field for the user's first name.
    last_name : StringField
        Field for the user's last name.
    email : StringField
        Field for the user's email address.
    phone_number : StringField
        Field for the user's phone number.
    company_name : StringField
        Field for the user's company name.
    street : StringField
        Field for the user's street address.
    postcode : StringField
        Field for the user's postcode.
    city : StringField
        Field for the user's city.
    country : StringField
        Field for the user's country.
    siren : StringField
        Field for the user's SIREN number.
    bundle : RadioField
        Field for selecting a bundle (Standard or Analytics).
    password : PasswordField
        Field for the user's password.
    confirm_password : PasswordField
        Field for confirming the user's password.
    submit : SubmitField
        Button for submitting the form.

    Methods
    -------
    validate_email(email)
        Validates the uniqueness of the email address.
    """
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])    
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])      
    street = StringField('Street', validators=[DataRequired(), Length(min=2, max=20)])     
    postcode = StringField('Postcode', validators=[DataRequired(), Length(min=2, max=20)])      
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])    
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=20)])   
    siren = StringField('Siren', validators=[DataRequired(), Length(min=2, max=20)])   
    bundle = RadioField('Select Bundle', choices=[('1','Standard'),('2','Analytics')], validators=[DataRequired()], default='2')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    Form for user login.

    This form allows users to login by providing their email and password.

    Attributes
    ----------
    email : StringField
        Field for the user's email address.
    password : PasswordField
        Field for the user's password.
    remember : BooleanField
        Field for remembering the user's session.
    submit : SubmitField
        Button for submitting the form.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    Form for updating user account details.

    This form allows users to update their personal and company details.

    Attributes
    ----------
    first_name : StringField
        Field for the user's first name.
    last_name : StringField
        Field for the user's last name.
    email : StringField
        Field for the user's email address.
    phone_number : StringField
        Field for the user's phone number.
    company_name : StringField
        Field for the user's company name.
    street : StringField
        Field for the user's street address.
    postcode : StringField
        Field for the user's postcode.
    city : StringField
        Field for the user's city.
    country : StringField
        Field for the user's country.
    siren : StringField
        Field for the user's SIREN number.
    bundle : RadioField
        Field for selecting a bundle (Standard or Analytics).
    picture : FileField
        Field for updating the user's profile picture.
    submit : SubmitField
        Button for submitting the form.

    Methods
    -------
    validate_email(email)
        Validates the uniqueness of the email address.
    """
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])    
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])      
    street = StringField('Street', validators=[DataRequired(), Length(min=2, max=20)])     
    postcode = StringField('Postcode', validators=[DataRequired(), Length(min=2, max=20)])      
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])    
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=20)])   
    siren = StringField('Siren', validators=[DataRequired(), Length(min=2, max=20)])   
    bundle = RadioField('Select Bundle', choices=[('1','Standard'),('2','Analytics')], validators=[DataRequired()], default='2')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choo se a different one.')


class RequestResetForm(FlaskForm):
    """
    Form for requesting password reset.

    This form allows users to request a password reset by providing their email address.

    Attributes
    ----------
    email : StringField
        Field for the user's email address.
    submit : SubmitField
        Button for submitting the form.

    Methods
    -------
    validate_email(email)
        Validates the existence of the email address.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    """
    Form for resetting password.

    This form allows users to reset their password by providing a new password.

    Attributes
    ----------
    password : PasswordField
        Field for the user's new password.
    confirm_password : PasswordField
        Field for confirming the user's new password.
    submit : SubmitField
        Button for submitting the form.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
    
class UploadForm(FlaskForm):
    """
    Form for uploading files.

    This form allows users to upload files with a title and text description.

    Attributes
    ----------
    title : StringField
        Field for the title of the file.
    body : TextAreaField
        Field for the text description of the file.
    dt : StringField
        Field for the date of the file.
    submit : SubmitField
        Button for submitting the form.
    """
    title = StringField('Title')
    body = TextAreaField('Text', render_kw={"rows": 10, "cols": 10})
    dt = StringField(validators=[DataRequired()])
    submit = SubmitField('Upload')

class TableForm(FlaskForm):
    """
    Form for updating tables.

    This form allows users to select a date and update tables accordingly.

    Attributes
    ----------
    opts : SelectField
        Field for selecting a date.
    submit : SubmitField
        Button for updating the table.
    """
    opts = SelectField('Date', choices=[])
    submit = SubmitField('Update')
