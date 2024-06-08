from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
)


class UploadForm(FlaskForm):
    """
    A form for uploading content with a title, body text, and a date.

    Attributes
    ----------
    title : StringField
        A text field for entering the title.
    body : TextAreaField
        A text area for entering the body text, with a specified number of rows and columns.
    dt : StringField
        A text field for entering the date, which is required.
    submit : SubmitField
        A submit button to trigger the form submission, labeled 'Upload'.
    """
    title = StringField('Title')
    body = TextAreaField('Text', render_kw={"rows": 10, "cols": 10})
    dt = StringField(validators=[DataRequired()])
    submit = SubmitField('Upload')


class TableForm(FlaskForm):
    """
    A form for selecting a date to update a table.

    Attributes
    ----------
    opts : SelectField
        A dropdown field for selecting the date.
    submit : SubmitField
        A submit button to trigger the form submission, labeled 'Update'.
    """
    opts = SelectField('Date', choices=[])
    submit = SubmitField('Update')


class GraphForm(FlaskForm):
    """
    A form for configuring and updating a graph with multiple series and chart types.

    Attributes
    ----------
    opts : SelectField
        A dropdown field for selecting the date.
    series_1 : SelectField
        A dropdown field for selecting the first series for the graph.
    series_2 : SelectField
        A dropdown field for selecting the second series for the graph.
    series_3 : SelectField
        A dropdown field for selecting the third series for the graph.
    types : list of tuple
        A list of tuples representing the available chart types.
    type_1 : SelectField
        A dropdown field for selecting the chart type for the first series, default is 'area'.
    type_2 : SelectField
        A dropdown field for selecting the chart type for the second series, default is 'line'.
    type_3 : SelectField
        A dropdown field for selecting the chart type for the third series, default is 'column'.
    submit1 : SubmitField
        A submit button to trigger the form submission for the first update, labeled 'Update'.
    submit2 : SubmitField
        A submit button to trigger the form submission for the second update, labeled 'Update'.
    """
    opts = SelectField('Date', choices=[])
    # chart series
    series_1 = SelectField('Bilan (1)', choices=[])
    series_2 = SelectField('Bilan (2)', choices=[])
    series_3 = SelectField('Bilan (3)', choices=[])
    # chart type
    types = [('area', 'Area'), ('line', 'Line'), ('column', 'Column')]
    type_1 = SelectField('Series 1', choices=types, default='area')
    type_2 = SelectField('Series 2', choices=types, default='line')
    type_3 = SelectField('Series 3', choices=types, default='column')

    submit1 = SubmitField('Update')
    submit2 = SubmitField('Update')
