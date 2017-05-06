from flask import Blueprint, render_template, request, session, flash, redirect, url_for, abort
from webapp.models import User, Likes, db, Task, Comment
from flask_login import login_required, current_user
from webapp.form import CommentForm

people_blueprint = Blueprint(
    'people',
    __name__
)


@people_blueprint.route('/<username>')
@login_required
def people(username):
    display_user = User.query.filter_by(username=username).first()

    # 完成时间倒序
    if current_user in display_user.following.all():
        tasks = Task.query.filter(Task.user_id == display_user.id, Task.public_level.in_([2, 3])).order_by(Task.status.asc(),Task.deadline.asc(), Task.id.asc()).all()
    elif current_user == display_user:
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all()
    else:
        tasks = Task.query.filter(Task.user_id == display_user.id, Task.public_level == 3).order_by(Task.status.asc(),Task.deadline.asc(), Task.id.asc()).all()

    return render_template('people/people.html',
                           display_user=display_user,
                           tasks=tasks
                           )


@people_blueprint.route('/<username>/following')
@login_required
def following(username):
    display_user = User.query.filter_by(username=username).first()
    people_list = display_user.following.all()
    return render_template('explore/home.html',
                           page_title='{}关注的人'.format(username),
                           people_list=people_list,
                           display_user=display_user
                           )


@people_blueprint.route('/<username>/follower')
@login_required
def follower(username):
    display_user = User.query.filter_by(username=username).first()
    people_list = display_user.follower.all()
    return render_template('explore/home.html',
                           page_title='关注{}的人'.format(username),
                           people_list=people_list,
                           display_user=display_user
                           )


@people_blueprint.route('/do')
@login_required
def do():

    # 关注模块
    follow_id = request.args.get('follow_id')
    if follow_id:
        if int(follow_id) != current_user.id:
            if current_user.check_following(follow_id):
                current_user.cancel_following(follow_id)
            else:
                current_user.add_following(follow_id)
        return 'follow success'

    # 点赞模块
    like_task_id = request.args.get('like_task_id')
    if like_task_id:
        like = Likes.query.filter(Likes.user_id == session['user_id'], Likes.task_id == like_task_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return 'like action success'
        else:
            do_like = Likes()
            try:
                do_like.i_like(like_task_id)
                db.session.add(do_like)
                db.session.commit()
            except:
                return 'like failed'
            else:
                return 'like action success'
