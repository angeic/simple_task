from flask import Blueprint, url_for, redirect, render_template, flash, session
from webapp.models import User, Task, db
from webapp.form import TaskForm, EditForm, DoneForm
from flask_login import login_required
from datetime import datetime

task_blueprint = Blueprint(
    'task',
    __name__
)


@task_blueprint.route('/', methods=['POST', 'GET'])
@login_required
def main():
    user = User.query.filter_by(id=session['user_id']).first()
    tasks = Task.query.filter_by(user_id=user.id).filter(Task.status != 1).order_by(Task.deadline.asc(), Task.create_time.asc()).all()
    form = DoneForm()
    if form.validate_on_submit():
        task = Task.query.filter_by(id=form.task_id.data).first()
        if session['user_id'] == task.user_id:
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
                           title='任务列表',
                           tasks=tasks,
                           user=user,
                           form=form
                           )


@task_blueprint.route('/done')
@login_required
def done():
    user = User.query.filter_by(id=session['user_id']).first()
    tasks = Task.query.filter_by(user_id=user.id).filter_by(status=1).order_by(Task.deadline.asc(), Task.create_time.asc()).all()
    return render_template('task/task.html',
                           title='已完成',
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
    return render_template('task/task_form.html',
                           form=form,
                           user=user,
                           title='创建任务'
                           )


@task_blueprint.route('/edit/<int:task_id>', methods=['POST', 'GET'])
@login_required
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    user = User.query.filter_by(id=session['user_id']).first()
    if task.user_id != user.id:
        flash('对不起，只有创建人才能修改任务，您无权限修改该任务！', category='warning')
        return redirect(url_for('task.main'))
    if task.status == 1 and task.user_id == user.id:
        flash('该任务已经完成，无法再修改', category='warning')
        return redirect(url_for('task.main'))

    form = EditForm()
    if form.validate_on_submit():
        Task.query.filter_by(id=task_id).update({
            'title': form.title.data,
            'text': form.text.data,
            'deadline': form.deadline.data,
            'public_level': form.public_level.data
        })
        db.session.commit()
        flash('任务修改成功！', category='info')
        return redirect(url_for('task.main'))

    form.title.data = task.title
    form.text.data = task.text
    form.deadline.data = task.deadline
    form.public_level.data = task.public_level
    return render_template('task/task_form.html',
                           form=form,
                           user=user,
                           title='编辑任务'
                           )

