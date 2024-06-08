from flask import render_template, Blueprint
from flask_login import login_required


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    """
    Render the home page.

    This view function handles the routes for the home page. It requires the user to be logged in.

    Returns
    -------
    str
        The rendered home page template.
    """
    return render_template('home.html')


@main.route('/admin')
@login_required
def admin():
    """
    Render the admin page.

    This view function handles the route for the admin page. It requires the user to be logged in.

    Returns
    -------
    str
        The rendered admin page template.
    """
    return render_template('admin/index.html')
