from flask import Blueprint, url_for, redirect, render_template, flash, session, g, abort, request
from webapp.models import Task, db, Comment
from webapp.form import TaskForm, EditForm, CommentForm
from flask_login import login_required, current_user
from datetime import datetime

circle_blueprint = Blueprint(
    'circle',
    __name__
)


@circle_blueprint.route('/')
@login_required
def home():
    return render_template('circle/home.html',
                           page_title='朋友圈动态',
                           )


@circle_blueprint.route('/following')
@login_required
def following():
    people_list = current_user.following.all()
    return render_template('circle/circle.html',
                           page_title='我关注的人',
                           people_list=people_list
                           )


@circle_blueprint.route('/follower')
@login_required
def follower():
    people_list = current_user.follower.all()
    return render_template('circle/circle.html',
                           page_title='关注我的人',
                           people_list=people_list
                           )


@circle_blueprint.route('/explore')
@login_required
def explore():
    tasks = Task.query.filter_by(public_level=3).order_by(Task.create_time.desc()).all()
    return render_template('circle/home.html',
                           page_title='发现',
                           tasks=tasks
                           )