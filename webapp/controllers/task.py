from flask import Blueprint, url_for, redirect, render_template, flash, session, g, abort, request
from webapp.models import Task, db, Comment
from webapp.form import TaskForm, EditForm, CommentForm
from flask_login import login_required, current_user
from datetime import datetime

task_blueprint = Blueprint(
    'task',
    __name__
)


@task_blueprint.route('/', methods=['POST', 'GET'])
@login_required
def main():
    # 最后期限倒序
    tasks = Task.query.filter(Task.user_id == current_user.id, Task.status != 1).order_by(Task.deadline.asc(), Task.create_time.asc()).all()
    return render_template('task/task.html',
                           page_title='任务列表',
                           tasks=tasks,
                           )


@task_blueprint.route('/done')
@login_required
def done():
    # 完成时间倒序
    tasks = Task.query.filter(Task.user_id == current_user.id, Task.status == 1).order_by(Task.create_time.desc()).all()
    return render_template('task/task.html',
                           page_title='已完成',
                           tasks=tasks
                           )


@task_blueprint.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(form.title.data)
        task.text = form.text.data
        task.deadline = form.deadline.data
        task.user_id = current_user.id
        task.public_level = form.public_level.data
        db.session.add(task)
        db.session.commit()
        flash('任务创建成功！', category='info')
        return redirect(url_for('task.main'))
    return render_template('task/task_new.html',
                           form=form,
                           page_title='创建任务',
                           now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                           )


@task_blueprint.route('/edit/<int:task_id>', methods=['POST', 'GET'])
@login_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if task.status == 9:
        abort(404)
    if current_user != task.user:
        abort(403)

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
                           task=task
                           )


@task_blueprint.route('/<int:task_id>', methods=['POST', 'GET'])
@login_required
def page(task_id):
    task = Task.query.get_or_404(task_id)
    if task.status == 9:
        abort(404)
    if current_user != task.user:
        abort(403)
    comment_form = CommentForm()
    comments = Comment.query.filter_by(task_id=task.id).order_by(Comment.date).all()
    if comment_form.validate_on_submit():
        new_comment = Comment()
        new_comment.text = comment_form.text.data
        new_comment.task_id = task.id
        new_comment.user_id = current_user.id
        db.session.add(new_comment)
        db.session.commit()
        flash('评论提交成功', category='info')
        return redirect(url_for('task.page', task_id=task.id))
    return render_template('task/task_page.html',
                           task=task,
                           comments=comments,
                           comment_form=comment_form
                           )


@task_blueprint.route('/do')
@login_required
def do():
    task_id = request.args.get('id')
    task = Task.query.get_or_404(task_id)

    if current_user.id == task.user_id:

        comment_switch = request.args.get('comment')
        if comment_switch in ['0', '1']:
            Task.query.filter_by(id=task_id).update({
                'comment_allowed': int(comment_switch)
            })

        task_delete = request.args.get('delete')
        if task_delete:
            db.session.delete(task)

        task_done = request.args.get('done')
        if task_done and task.status != 1:
            Task.query.filter_by(id=task_id).update({
                'status': 1,
                'overtime': task.is_overtime(),
                'done_time': datetime.now()
            })

        db.session.commit()
        return 'hello'

    else:
        abort(403)
