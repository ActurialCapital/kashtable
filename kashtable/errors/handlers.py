from flask import Blueprint, render_template
from kashtable.errors.forms import RedirectHomeForm

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """
    Handle 404 errors by rendering a custom 404 error page.

    Parameters
    ----------
    error : werkzeug.exceptions.NotFound
        The 404 error that was raised.

    Returns
    -------
    tuple
        A tuple containing the rendered 404 error page template and the 404 status code.
    """
    form = RedirectHomeForm()
    return render_template('errors/404.html', form=form), 404


@errors.app_errorhandler(403)
def error_403(error):
    """
    Handle 403 errors by rendering a custom 403 error page.

    Parameters
    ----------
    error : werkzeug.exceptions.Forbidden
        The 403 error that was raised.

    Returns
    -------
    tuple
        A tuple containing the rendered 403 error page template and the 403 status code.
    """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """
    Handle 500 errors by rendering a custom 500 error page.

    Parameters
    ----------
    error : werkzeug.exceptions.InternalServerError
        The 500 error that was raised.

    Returns
    -------
    tuple
        A tuple containing the rendered 500 error page template and the 500 status code.
    """
    return render_template('errors/500.html'), 500
