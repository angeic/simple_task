from flask import Blueprint, render_template, session
from webapp.models import Task
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import or_, and_

circle_blueprint = Blueprint(
    'circle',
    __name__
)


@circle_blueprint.route('/')
@login_required
def home():
    following = current_user.following.all()
    tasks = Task.query.filter(
            or_(and_(Task.user_id.in_([user.id for user in following]), Task.public_level == '3'),  # 我关注的
                and_(Task.user_id.in_([user.id for user in current_user.friends()]), Task.public_level == '2'),  # 互相关注的
                Task.user_id == session['user_id'])  # 自己的
    ).order_by(Task.create_time.desc()).all()
    return render_template('circle/home.html',
                           page_title='圈子动态',
                           tasks=tasks,
                           )
