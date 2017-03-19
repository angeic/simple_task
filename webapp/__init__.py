from flask import Flask, redirect, url_for, render_template, session, flash
from webapp.config import DevConfig
from .models import db, User, Task
from .form import LoginForm, RegisterForm
from flask_login import login_user, logout_user,login_required, current_user
from webapp.extensions import login_manager
from .controllers.task import task_blueprint
from .controllers.people import people_blueprint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(task_blueprint, url_prefix='/task')
    app.register_blueprint(people_blueprint, url_prefix='/people')

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if 'user_id' in session:
            return redirect(url_for('task.main'))
        login_form = LoginForm()
        register_form = RegisterForm()
        if register_form.validate_on_submit():
            flash('注册成功，请登录', category='success')
            return redirect(url_for('index'))
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            login_user(user, remember=login_form.remember.data)
            flash('欢迎回来，{}'.format(user.username), category='success')
        return render_template('index.html', login_form=login_form, register_form=register_form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def error_500(error):
        return render_template('500.html'), 500

    return app
