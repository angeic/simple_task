from flask import Blueprint, url_for, redirect, render_template, flash, session, g, abort
from webapp.models import User, Task, db, Comment
from webapp.form import TaskForm, EditForm, DoneForm, CommentForm
from flask_login import login_required
from datetime import datetime

task_blueprint = Blueprint(
    'task',
    __name__
)


@task_blueprint.before_request
def check_user():
    if 'user_id' in session:
        g.current_user = User.query.filter_by(id=int(session['user_id'])).one()
    else:
        g.current_user = None


@task_blueprint.route('/', methods=['POST', 'GET'])
@login_required
def main():
    user = User.query.filter_by(id=session['user_id']).first()
    tasks = Task.query.filter_by(user_id=user.id).filter(Task.status != 1).order_by(Task.deadline.asc(), Task.create_time.asc()).all()
    form = DoneForm()
    if form.validate_on_submit():
        task = Task.query.filter_by(id=form.task_id.data).first()
        if session['user_id'] == str(task.user_id):
            Task.query.filter_by(id=form.task_id.data).update({
                'status': 1,
                'done_time': datetime.now(),
                'overtime': task.is_overtime()
            })
            db.session.commit()
            flash('任务成功完成！', category='info')
            return redirect(url_for('task.main'))
        else:
            flash('操作异常，请重新操作', category='warning')
    return render_template('task/task.html',
                           page_title='任务列表',
                           tasks=tasks,
                           user=user,
                           form=form,
                           )


@task_blueprint.route('/done')
@login_required
def done():
    user = User.query.filter_by(id=session['user_id']).first()
    tasks = Task.query.filter_by(user_id=user.id).filter_by(status=1).order_by(Task.deadline.asc(), Task.create_time.asc()).all()
    return render_template('task/task.html',
                           page_title='已完成',
                           tasks=tasks,
                           user=user,
                           )


@task_blueprint.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    user = User.query.filter_by(id=session['user_id']).first()
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(form.title.data)
        task.text = form.text.data
        task.deadline = form.deadline.data
        task.user_id = user.id
        task.public_level = form.public_level.data
        db.session.add(task)
        db.session.commit()
        flash('任务创建成功！', category='info')
        return redirect(url_for('task.main'))
    return render_template('task/task_new.html',
                           form=form,
                           user=user,
                           page_title='创建任务',
                           now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                           )


@task_blueprint.route('/edit/<int:task_id>', methods=['POST', 'GET'])
@login_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if g.current_user != task.user:
        abort(403)
    user = User.query.filter_by(id=session['user_id']).first()

    form = EditForm()
    if form.validate_on_submit():
        if task.status == 1:
            Task.query.filter_by(id=task_id).update({
                'public_level': form.public_level.data,
                'comment_allowed': form.comment_allowed.data
            })
            db.session.commit()
            flash('任务修改成功！', category='info')
            return redirect(url_for('task.page', task_id=task.id))
        else:
            Task.query.filter_by(id=task_id).update({
                'title': form.title.data,
                'text': form.text.data,
                'deadline': form.deadline.data,
                'public_level': form.public_level.data,
                'comment_allowed': form.comment_allowed.data
            })
            db.session.commit()
            flash('任务修改成功！', category='info')
            return redirect(url_for('task.page', task_id=task.id))
    if task.status == 1:
        flash('该任务已经完成，只能修改隐私和评论状态', category='info')
    form.title.data = task.title
    form.text.data = task.text
    form.deadline.data = task.deadline
    form.public_level.data = task.public_level
    form.comment_allowed.data = task.comment_allowed
    return render_template('task/task_edit.html',
                           form=form,
                           task=task,
                           user=user
                           )


@task_blueprint.route('/<int:task_id>', methods=['POST', 'GET'])
@login_required
def page(task_id):
    task = Task.query.get_or_404(task_id)
    if g.current_user != task.user:
        abort(403)
    user = User.query.filter_by(id=session['user_id']).first()
    comment_form = CommentForm()
    done_form = DoneForm()
    comments = Comment.query.filter_by(task_id=task.id).order_by(Comment.date).all()
    if done_form.validate_on_submit():
        if session['user_id'] == str(task.user_id):
            Task.query.filter_by(id=task.id).update({
                'status': 1,
                'done_time': datetime.now(),
                'overtime': task.is_overtime()
            })
            db.session.commit()
            flash('任务成功完成！', category='info')
            return redirect(url_for('task.page', task_id=task.id))
    if comment_form.validate_on_submit():
        new_comment = Comment()
        new_comment.text = comment_form.text.data
        new_comment.task_id = task.id
        new_comment.user_id = user.id
        db.session.add(new_comment)
        db.session.commit()
        flash('评论提交成功', category='info')
        return redirect(url_for('task.page', task_id=task.id))
    return render_template('task/task_page.html',
                           task=task,
                           user=user,
                           comments=comments,
                           comment_form=comment_form,
                           done_form=done_form
                           )
