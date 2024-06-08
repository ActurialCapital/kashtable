from flask_login import login_user, current_user, logout_user, login_required
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    Blueprint,
)

from kashtable import db, bcrypt
from kashtable.models import User
from kashtable.users.utils import save_picture, send_reset_email
from kashtable.config import Config
from kashtable.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register new user.

    Returns
    -------
    Redirect
        Redirect to login page on successful registration, otherwise renders registration form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            bundle=form.bundle.data,
            company_name=form.company_name.data,
            street=form.street.data,
            postcode=form.postcode.data,
            city=form.city.data,
            country=form.country.data,
            siren=form.siren.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template(
        'register.html',
        title='Register',
        form=form,
    )


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    User login.

    Returns
    -------
    Redirect
        Redirect to appropriate page based on login status and user roles, or renders login form.
    """
    if current_user.is_authenticated:
        if current_user.activated:
            return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if current_user.activated:
                next_page = request.args.get('next')
                if next_page:
                    if current_user.email == Config.BASIC_AUTH_USERNAME:
                        return redirect(url_for('main.admin'))
                    else:
                        return redirect(next_page)
                elif current_user.email == Config.BASIC_AUTH_USERNAME:
                    return redirect(url_for('main.admin'))
                else:
                    return redirect(url_for('main.home'))
            else:
                flash('Your account has been disactivated. Please contact us', 'danger')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template(
        'login.html',
        title='Login',
        form=form,
    )


@users.route("/logout")
def logout():
    """
    User logout.

    Returns
    -------
    Redirect
        Redirect to home page.
    """
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """
    User profile page.

    Returns
    -------
    Rendered Template
        Renders user profile page with update form.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.company_name = form.company_name.data
        current_user.street = form.street.data
        current_user.postcode = form.postcode.data
        current_user.city = form.city.data
        current_user.country = form.country.data
        current_user.siren = form.siren.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.company_name.data = current_user.company_name
        form.street.data = current_user.street
        form.postcode.data = current_user.postcode
        form.city.data = current_user.city
        form.country.data = current_user.country
        form.siren.data = current_user.siren
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template(
        'profile.html',
        title='Profile',
        image_file=image_file,
        form=form,
    )


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    Request password reset.

    Returns
    -------
    Redirect
        Redirect to login page after sending reset email, or renders reset password request form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_request.html',
        title='Reset Password',
        form=form,
    )


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    Reset password token validation.

    Parameters
    ----------
    token : str
        Token for password reset.

    Returns
    -------
    Redirect
        Redirect to login page on successful password reset, or renders reset password form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_token.html',
        title='Reset Password',
        form=form,
    )
