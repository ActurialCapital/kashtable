import dateutil
import os
import pandas as pd
import numpy as np
from flask_login import current_user, login_required
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    Blueprint,
    current_app,
    g,
    session
)
from kashtable.models import File
from kashtable.posts import utils
from kashtable.posts.forms import UploadForm, TableForm, GraphForm


posts = Blueprint('posts', __name__)


@posts.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Handle file upload functionality for logged-in users.

    This view function manages the file upload process, allowing users to upload 
    files, which are then saved to the server. The function also creates a directory 
    for the user if it doesn't already exist.

    Returns
    -------
    str
        The rendered upload page template if the request method is GET or the form 
        validation fails.
    werkzeug.wrappers.response.Response
        A redirect to the home page if the file is successfully uploaded.
    """
    form = UploadForm()
    user_email = str(current_user.email)
    try:
        os.mkdir(os.path.join(current_app.root_path, 'files/raw/' + user_email))
    except OSError:
        pass
    if request.method == 'POST':
        if form.validate_on_submit():
            file = request.get_array(field_name='file')
            df = pd.DataFrame(file)
            path = current_app.root_path
            name = str(form.dt.data)

            with pd.ExcelWriter(os.path.join(path, f'files/raw/{user_email}/{name}.xlsx')) as writer:
                df.to_excel(writer)

            with open(os.path.join(path, f'files/raw/{user_email}/{name}.txt'), "w") as text_file:
                print(
                    f"Title: {form.title.data}\nBody: {form.body.data}", file=text_file)

            flash('File has been uploaded successfuly!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('OOPS! Something went wrong here! Please try again.', 'danger')
    return render_template('user_upload.html', form=form)


@posts.before_request
def before_request():
    """
    Set the global user object before each request.

    This function checks if there is a 'user' in the session and sets the global user 
    object accordingly.
    """
    g.user = None
    if 'user' in session:
        g.user = session['user']


@posts.route('/<string:table_name>', methods=['GET', 'POST'])
@login_required
def table(table_name):
    """
    Display and update a table based on the selected date.

    This view function handles the display and update of a table. The table is filtered 
    based on the selected date and the table name.

    Parameters
    ----------
    table_name : str
        The name of the table to display.

    Returns
    -------
    str
        The rendered table page template.
    werkzeug.wrappers.response.Response
        A redirect to the upload page if there are no materials to display.
    """
    def refresh(doc):
        """
        Filter out table using table_name column in pandas.DataFrame object.

        Parameters
        ----------
        doc : list
            A list of documents to be normalized and filtered.

        Returns
        -------
        pandas.io.formats.style.Styler
            A styled DataFrame object for rendering.

        Note
        ----
        Do not modify uuid=table1, as it matches $("#T_table1").DataTable() 
        in template. Also, "T_" is created by pandas.DataFrame().style.render() located in .users.render.table class. 
        For more information visit pandas.pydata.org.
        """
        doc = pd.json_normalize(doc)
        # filter to access spec table
        df = doc.loc[doc["table_name"] == table_name]
        return utils.ExcelFormatter(df, uuid='table1').financials()

    form = TableForm()
    user = File.query.filter_by(user_id=current_user.id)
    try:
        file = user.order_by(File.date.desc()).first()
        form.opts.choices = [(item.id, item.date.strftime('%B %Y'))
                             for item in user.all()]

        try:
            if request.method == 'POST':
                ufile = user.filter_by(id=form.opts.data).first()
                tb = refresh(ufile.doc)
                session.pop('user', None)
                session['user'] = form.opts.data
                flash(f"Updated as at {ufile.date.strftime('%B %Y')}.", 'info')
                return render_template('table.html', title=table_name, tb=tb, form=form)
            elif session['user'] == None:  # before first request
                tb = refresh(file.doc)
                flash(f"Updated as at {file.date.strftime('%B %Y')}.", 'info')
            else:
                ufile = user.filter_by(id=session['user']).first()
                form.opts.data = session['user']
                tb = refresh(ufile.doc)
                flash(f"Updated as at {ufile.date.strftime('%B %Y')}.", 'info')
            return render_template(
                'table.html',
                title=table_name,
                tb=tb,
                form=form,
            )
        except:
            tb = refresh(file.doc)
            flash(f"Updated as at {file.date.strftime('%B %Y')}.", 'info')
            return render_template(
                'table.html',
                title=table_name,
                tb=tb,
                form=form,
            )
    except:
        flash('OOPS! There is no materials to display!', 'danger')
        flash('Please contact us and upload a project.', 'info')
        return redirect(url_for('posts.upload'))


@posts.route('/graph', methods=['GET', 'POST'])
@login_required
def graph():
    """
    Display and update a graph based on the selected series and chart types.

    This view function handles the display and update of a graph. The graph can be 
    configured with different series and chart types.

    Returns
    -------
    str
        The rendered graph page template.
    """
    def reshape(doc):
        """
        Reshape the document into a DataFrame suitable for graphing.

        Parameters
        ----------
        doc : list
            A list of documents to be normalized and reshaped.

        Returns
        -------
        pandas.DataFrame
            A reshaped DataFrame object.
        """
        doc = pd.json_normalize(doc)
        df = doc.loc[doc["table_name"].isin([
            'Bilan',
            'Compte de Resultat Analytique Cumulé'
        ])]
        labels = 'Description'
        formatter = [
            'table_name',
            'font_weight',
            'font_color',
            'background_color',
            'font_family',
            'font_size',
            'text_align',
            'sort_by'
        ]
        dt = list(df.loc[:, ~df.columns.isin(formatter)
                         ].drop(labels, axis=1).columns)
        dt_formatted = [str(dateutil.parser.parse(
            d).strftime("%b %Y")) for d in dt]
        df = df.rename(columns=dict(zip(dt, dt_formatted)))
        df = df.drop(formatter, axis=1)
        df = df.set_index(labels)
        df = df.dropna(axis=1, how='all')
        df = df.replace(np.nan, 'null')
        df = round(df, 0)
        return df

    form = GraphForm()
    user = File.query.filter_by(user_id=current_user.id)

    file = user.order_by(File.date.desc()).first()
    doc = file.doc
    df = reshape(doc)

    form.opts.choices = [(item.id, item.date.strftime('%B %Y'))
                         for item in user.all()]

    choice_labels = [(label, label) for _, label in enumerate(df.index)]

    choice_labels.append(("--", "--"))

    form.series_1.choices = choice_labels
    form.series_2.choices = choice_labels
    form.series_3.choices = choice_labels

    if request.method == 'POST':
        # ufile = user.filter_by(id=form.opts.data).first()
        # df = reshape(ufile.doc)
        # flash(f"Updated as at {ufile.date.strftime('%B %Y')}.", 'info')
        return render_template(
            'graph.html',
            title='Dashboard',
            chart_id='chart1',
            df=df,
            form=form
        )

    # default
    form.series_1.data = "Chiffre d'affaires"
    form.series_2.data = "--"
    form.series_3.data = "--"

    return render_template(
        'graph.html',
        title='Dashboard',
        chart_id='chart1',
        df=df,
        form=form,
    )
