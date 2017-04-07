from flask import Flask, redirect, url_for, render_template, session, flash, g, request
from webapp.config import DevConfig
from .models import db, User, Task
from .form import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from webapp.extensions import login_manager
from .controllers.task import task_blueprint
from .controllers.people import people_blueprint
from .controllers.weibo import weibo_blueprint
from .controllers.login import login_blueprint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(task_blueprint, url_prefix='/task')
    app.register_blueprint(people_blueprint, url_prefix='/people')
    app.register_blueprint(weibo_blueprint, url_prefix='/wb')
    app.register_blueprint(login_blueprint,url_prefix='/login')

    @app.route('/')
    def home():
        return redirect(url_for('task.main'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login.index'))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def error_500(error):
        return render_template('500.html'), 500

    return app
