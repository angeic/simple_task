from flask import Blueprint, render_template
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

    follower = current_user.follower.all()
    following = current_user.following.all()
    tasks = Task.query.filter(
              or_(and_(Task.user_id.in_([user.id for user in follower]), Task.public_level.in_([2, 3])),
        and_(Task.user_id.in_([user.id for user in following]), Task.public_level == '3'))
    ).order_by(Task.create_time.desc()).all()
    return render_template('circle/home.html',
                           page_title='朋友圈动态',
                           tasks=tasks,
                           follower=follower,
                           following=following
                           )
