from flask import Blueprint, render_template, request, session, flash, redirect, url_for
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
    return render_template('people/people.html',
                           display_user=display_user
                           )


@people_blueprint.route('/task/<int:task_id>', methods=['POST', 'GET'])
@login_required
def task(task_id):
    task_it = Task.query.get_or_404(task_id)
    display_user = User.query.get(task_it.user_id)
    comment_form = CommentForm()
    comments = Comment.query.filter_by(task_id=task_it.id).order_by(Comment.date).all()
    if comment_form.validate_on_submit():
        new_comment = Comment()
        new_comment.text = comment_form.text.data
        new_comment.task_id = task.id
        new_comment.user_id = current_user.id
        db.session.add(new_comment)
        db.session.commit()
        flash('评论提交成功', category='info')
        return redirect(url_for('task.page', task_id=task.id))
    return render_template('people/task.html',
                           display_user=display_user,
                           task=task_it,
                           comment_form=comment_form,
                           comments=comments
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
