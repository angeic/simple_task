from flask import Blueprint, render_template, session
from webapp.models import Task, User
from flask_login import login_required, current_user

explore_blueprint = Blueprint(
    'explore',
    __name__
)


@explore_blueprint.route('/')
@login_required
def home():
    people_list = User.query.filter(User.id != session['user_id']).order_by(User.reg_date.desc()).all()
    tasks = Task.query.filter_by(public_level=3).order_by(Task.create_time.desc()).all()
    return render_template('explore/home.html',
                           page_title='发现',
                           tasks=tasks,
                           people_list=people_list,
                           display_user=current_user
                           )