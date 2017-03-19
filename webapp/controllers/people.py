from flask import Blueprint, url_for, redirect, render_template, flash, session
from webapp.models import User, Task
from webapp.form import LoginForm, RegisterForm
from flask_login import logout_user, login_user, login_required, current_user


people_blueprint = Blueprint(
    'people',
    __name__
)


@people_blueprint.route('/<username>')
@login_required
def people(username):
    user = User.query.filter_by(username=username).first()
    return render_template('people/people.html', user=user)