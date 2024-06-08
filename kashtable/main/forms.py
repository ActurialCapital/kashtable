from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    DateField
)


class UploadAdminForm(FlaskForm):
    """
    A form for administrators to upload files with associated metadata.

    Attributes
    ----------
    opts : SelectField
        A dropdown field for selecting the user, which is required.
    dt : DateField
        A field for entering the date, which is required.
    name : StringField
        A text field for entering the file name, which is required.
    submit : SubmitField
        A submit button to trigger the form submission, labeled 'Upload'.
    """
    opts = SelectField('User', choices=[], validators=[DataRequired()])
    dt = DateField('Date', validators=[DataRequired()])
    name = StringField('File Name', validators=[DataRequired()])
    submit = SubmitField('Upload')
