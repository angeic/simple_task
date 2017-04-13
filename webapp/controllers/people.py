from flask import Blueprint, render_template, request, session
from webapp.models import User, Likes, db, Task
from flask_login import login_required, current_user


people_blueprint = Blueprint(
    'people',
    __name__
)


@people_blueprint.route('/<username>')
@login_required
def people(username):
    display_user = User.query.filter_by(username=username).first()
    return render_template('people/people.html',
                           display_user=display_user
                           )


@people_blueprint.route('/do')
@login_required
def do():
    follow_id = request.args.get('follow_id')
    if follow_id:
        if int(follow_id) != current_user.id:
            if current_user.check_following(follow_id):
                current_user.cancel_following(follow_id)
            else:
                current_user.add_following(follow_id)
        return 'follow success'

    # 点赞模块
    like_id = request.args.get('like_id')
    if like_id:
        like = Likes.query.filter(Likes.user_id == session['user_id'], Likes.task_id == like_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return 'unlike success'
        else:
            like = Likes()
            try:
                like.i_like(like_id)
                db.session.add(like)
                db.session.commit()
            except:
                return 'like failed'
            else:
                return 'like success'
