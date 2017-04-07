from flask import Blueprint, url_for, redirect, render_template, flash, session, request
from webapp.models import User
from flask_login import login_user
from webapp.form import LoginForm,RegisterForm

login_blueprint = Blueprint(
    'login',
    __name__
)


@login_blueprint.route('/', methods=['POST', 'GET'])
def index():
    if 'user_id' in session:
        return redirect(url_for('task.main'))
    action = request.args.get('action')
    login_form = LoginForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        flash('注册成功，请登录', category='success')
        return redirect(url_for('index'))
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        login_user(user, remember=login_form.remember.data)
        flash('欢迎回来，{}'.format(user.username), category='success')
        return redirect(url_for('task.main'))
    return render_template('index.html', login_form=login_form, register_form=register_form, action=action)


