import os
from datetime import date
import pandas as pd
import json
from markupsafe import Markup
import uuid
from flask import request, render_template
from flask_admin.model import typefmt
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from kashtable.models import AVAILABLE_USER_TYPES
from kashtable import bcrypt
from kashtable.config import Config
from kashtable.posts import utils


# Create directory for file fields to use
file_path = Config.FILE_PATH + '/archive'

try:
    os.mkdir(file_path)
except OSError:
    pass


class CustomPasswordField(PasswordField): 
    """
    Custom password field for hashing and setting user passwords.

    Methods
    -------
    populate_obj(obj, name)
        Populate the object's password attribute with a hashed password.

    """
    def populate_obj(self, obj, name):
        """
        Populate the object's password attribute with a hashed password.

        Parameters
        ----------
        obj : object
            The object to populate.
        name : str
            The name of the attribute to populate.

        Returns
        -------
        None

        """
        setattr(obj, name, bcrypt.generate_password_hash(self.data).decode('utf-8'))


class UserCRUD(ModelView):
    """
    Custom CRUD view for managing user data.

    Attributes
    ----------
    list_template : str
        The template for rendering the list view.
    page_size : int
        The number of items per page.
    can_set_page_size : bool
        Indicates whether users can set the page size.
    can_view_details : bool
        Indicates whether users can view details.
    can_export : bool
        Indicates whether users can export data.
    export_types : list
        List of export file formats.
    form_choices : dict
        Choices for form fields.
    form_widget_args : dict
        Additional arguments for form widgets.
    column_list : list
        List of columns to display in the list view.
    column_searchable_list : list
        List of columns to enable searching.
    column_editable_list : list
        List of columns that can be edited.
    column_details_list : list
        List of columns to display in the details view.
    form_columns : list
        List of fields to display in the create/edit form.
    form_create_rules : list
        List of fields required for creating a new entry.
    column_auto_select_related : bool
        Indicates whether related columns should be automatically loaded.
    column_default_sort : list
        Default sorting criteria.
    column_filters : list
        List of columns to filter by.
    form_extra_fields : dict
        Extra fields to include in the form.

    Methods
    -------
    None

    """
    list_template = 'admin/my_clients.html'
    page_size = 100
    can_set_page_size = True
    can_view_details = True
    can_export = True
    export_types = ['csv', 'xls']
    form_choices = {
        'type': AVAILABLE_USER_TYPES,
    }
    form_widget_args = {
        'id': {
            'readonly': True
        }
    }
    column_list = [
        'activated',
        'type',
        'bundle',
        'company_name',
        'email',
        'phone_number',
    ]
    column_searchable_list = [
        'company_name',
        'email',      
    ]
    column_editable_list = [
        'type', 
        'bundle', 
        'activated'
    ]
    column_details_list = [
        'id',
        'activated',
        'type',
        'bundle',
        'company_name',
        'first_name',
        'last_name',
        'email',
        'phone_number',        
        'street',
        'postcode',
        'city',
        'country',
        'siren',
        'password'

    ]
    form_columns = [
        'id',
        'type',
        'last_name',
        'first_name',
        'email',
        'company_name',
        'street',
        'postcode',
        'city',
        'country',
        'siren',        
        'phone_number',
        'bundle',
        'activated',
        'password'
    ]
    form_create_rules = [
        'type',
        'last_name',
        'first_name',
        'email',
        'company_name',
        'street',
        'postcode',
        'city',
        'country',
        'siren',     
        'phone_number',
        'bundle',
        'activated',
        'password'
    ]

    column_auto_select_related = True
    column_default_sort = [('type', False), ('company_name', False)]  # sort on multiple columns

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    column_filters = [
        'type',
        'last_name',
        'first_name',
        'email',
        'company_name',
        'street',
        'postcode',
        'city',
        'country',
        'siren',        
        'phone_number',
        'bundle',
        'activated',
    ]

    form_extra_fields = {
        'password': CustomPasswordField('Password')
    }
  

class FileCRUD(ModelView):
    """
    Custom CRUD view for managing file data.

    Attributes
    ----------
    list_template : str
        The template for rendering the list view.
    MY_DEFAULT_FORMATTERS : dict
        Default formatters for column types.
    column_type_formatters : dict
        Formatters for column types.
    form_args : dict
        Arguments for form fields.
    form_widget_args : dict
        Additional arguments for form widgets.

    Methods
    -------
    None

    """
    def _date_format(view, value):
        """
        Format date values.

        Parameters
        ----------
        view : object
            The view object.
        value : datetime.date
            The value to format.

        Returns
        -------
        str
            The formatted date.

        """
        return value.strftime('%B %Y')

    def _json_formatter(view, context, model, name):
        """
        Perform actions when a model is changed.

        Parameters
        ----------
        form : object
            The form used for the change.
        model : object
            The model object being changed.
        is_created : bool, optional
            Indicates whether the model is being created, by default False

        Returns
        -------
        None

        Note
        ----
        Format `model.doc` as it is extracted in route `posts.table` in order to
        give realistic reprensentation of the client side

        """
        value = getattr(model, name)
        df = pd.json_normalize(value)
        # split tables into different tabs
        list_tables = list(df['table_name'].drop_duplicates())
        items = {}
        for table_name in list_tables:  
            frame = df.loc[df['table_name'] == table_name]
            # dict table_name as key, tuple (id, rendered html tables)
            items.update( {table_name: ( uuid.uuid4(), utils.ExcelFormatter(frame).financials() )} )
        return Markup(render_template('admin/details.html', items=items))

    def on_model_change(self, form, model, is_created=False):
        """
        Perform actions when a model is changed.

        Parameters
        ----------
        form : object
            The form used for the change.
        model : object
            The model object being changed.
        is_created : bool, optional
            Indicates whether the model is being created, by default False

        Returns
        -------
        None

        """
        file = request.get_array(field_name='doc')
        df = pd.DataFrame(file)
        # convert first row to column header
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        df = df.apply( pd.to_numeric, errors='ignore')
        # load to db
        model.doc = json.loads(df.to_json(orient='records', date_format='iso'))


    list_template = 'admin/my_files.html'    
    MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
    MY_DEFAULT_FORMATTERS.update({
        date: _date_format       
    })    
    column_type_formatters = MY_DEFAULT_FORMATTERS
    form_args = dict(
        time = dict(validators=[DataRequired()],format='%B %Y')
    )
    form_widget_args = dict(
        time={'data-date-format': u'%B %Y'} 
    )
    page_size = 100
    can_set_page_size = True
    can_view_details = True
    can_edit = False
    column_list = [
        'user', 
        'name', 
        'date', 
    ]
    column_details_list = [
        'id',
        'user',
        'name',
        'date',
        'doc'             
    ]
    form_columns = [
        'user', 
        'name',
        'date',
        'doc',
    ]
    column_default_sort = [
        ('user.company_name', False), 
        ('user.email', False), 
        ('date', True)
    ]
    can_export = True
    export_types = ['csv', 'xls']
    column_sortable_list = [
        ('user', ('user.company_name', 'user.email')),  # sort on multiple columns
        'name',       
        'date',
    ]
    column_searchable_list = [
        'user.company_name',
        'user.email',
        'name',
        'date'
    ]
    column_filters = [
        'user.company_name',
        'user.email',
        'name',     
        'date',
    ]
    column_formatters = {
        'doc': _json_formatter,
    }    
    form_overrides = {
        'doc': FileUploadField
    }
    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'doc': {
            'label': 'Doc',
            'base_path': file_path,
            'allow_overwrite': True
        }
    }