from flask_wtf import FlaskForm
from wtforms import SubmitField


class RedirectHomeForm(FlaskForm):
    """
    A form for redirecting to the home page.

    This form includes a single submit button labeled 'Return Home'.

    Attributes
    ----------
    submit : SubmitField
        A submit button to trigger the form submission, labeled 'Return Home'.
    """
    submit = SubmitField('Return Home')
