from flask import Blueprint, url_for, redirect, render_template, flash, session
from webapp.models import User, Task
from webapp.form import LoginForm, RegisterForm
from flask_login import logout_user, login_user, login_required, current_user


task_blueprint = Blueprint(
    'task',
    __name__
)

@task_blueprint.route('/')
@login_required
def main():
    return render_template('task/task.html')




