from flask import Blueprint, url_for, redirect, render_template, flash, session, request
from webapp.models import User
from flask_login import login_user, current_user
from webapp.form import LoginForm, RegisterForm

login_blueprint = Blueprint(
    'login',
    __name__
)


@login_blueprint.route('/', methods=['POST', 'GET'])
def home():
    if 'user_id' in session:
        return redirect(url_for('task.home'))
    action = request.args.get('action')
    login_form = LoginForm()
    register_form = RegisterForm()

    if action != 'reg':
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            login_user(user, remember=login_form.remember.data)
            flash('欢迎回来，{}'.format(user.username), category='success')
            return redirect(url_for('task.home'))

    if action == 'reg':
        if register_form.validate_on_submit():
            user = User.query.filter_by(username=register_form.username.data).first()
            login_user(user, remember=False)
            flash('欢迎您，{}'.format(current_user.username), category='success')
            return redirect(url_for('task.home'))

    return render_template('index.html', login_form=login_form, register_form=register_form, action=action)


@login_blueprint.route('/check')
def check():
    if 'user_id' in session:
        return redirect(url_for('task.home'))
    else:
        return redirect(url_for('login.home'))
