from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func
from datetime import datetime
from flask import flash, session
db = SQLAlchemy()


follows = db.Table('follows',
                   db.Column('user_id', db.ForeignKey('user.id')),
                   db.Column('follow_id', db.ForeignKey('user.id'))
                   )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    bio = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), index=True)
    password = db.Column(db.String(255))
    reg_date = db.Column(db.TIMESTAMP(), server_default=func.now())
    last_login_date = db.Column(db.DateTime())
    wb_uid = db.Column(db.String(20))
    tasks = db.relationship(
        'Task',
        backref='user',
        lazy='dynamic'
    )

    following = db.relationship(
        'User',
        secondary=follows,
        primaryjoin=(follows.c.user_id == id),
        secondaryjoin=(follows.c.follow_id == id),
        backref=db.backref('follower', lazy='dynamic'),
        lazy='dynamic'
    )

    liked = db.relationship(
        'Likes',
        backref='user',
        lazy='dynamic'
    )

    # 检查是否关注了这个人
    def check_following(self, user_id):
        if User.query.get(user_id) in self.following.all():
            return True
        else:
            return False

    # 检查是否被这个人关注
    def check_follower(self, user_id):
        if User.query.get(user_id) in self.follower.all():
            return True
        else:
            return False

    def add_following(self, user_id):
        self.following.append(User.query.get_or_404(user_id))
        db.session.add(self)
        db.session.commit()

    def cancel_following(self, user_id):
        self.following.remove(User.query.get_or_404(user_id))
        db.session.add(self)
        db.session.commit()

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def count_task(self):
        return '创建了{}个任务，完成了{}个'.format(len(self.tasks.all()), len(self.tasks.filter_by(status=1).all()))

    def unfinish_task(self):
        return len(self.tasks.all()) - len(self.tasks.filter_by(status=1).all())

    def wb_reg(self, wb_uid):
        if not User.query.filter_by(wb_uid=wb_uid).first():
            self.wb_uid = wb_uid

    def relation(self):
        return list(set(current_user.following.all()) & set(self.follower.all()))


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), index=True)
    text = db.Column(db.Text())
    create_time = db.Column(db.TIMESTAMP(), server_default=func.now())
    update_time = db.Column(db.DateTime(), onupdate=func.now())
    done_time = db.Column(db.DateTime())
    deadline = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.SmallInteger(), default=0)  # 0：进行中 1：已完成 2：暂停 9：删除
    public_level = db.Column(db.SmallInteger(), default=3)  # 1：仅自己可见   2：我关注的人可见   3：所有人可见
    overtime = db.Column(db.Boolean, default=0)  # 任务结束后： 0：未超时 1：超时
    comment_allowed = db.Column(db.Boolean, default=1)  # 0：禁止评论并隐藏所有评论内容 1：允许评论
    comments = db.relationship(
        'Comment',
        backref='task',
        lazy='dynamic'
    )

    liked = db.relationship(
        'Likes',
        backref='task',
        lazy='dynamic'
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Task: {}|User:{}>'.format(self.title, self.user_id)

    def is_overtime(self):
        if self.status == 0 and self.deadline > datetime.now():
            return False
        elif self.status == 1 and self.overtime == 0:
            return False
        else:
            return True

    # 超时情况
    def over_time(self):
        if self.status == 0 and self.deadline < datetime.now():
            over_time = datetime.now() - self.deadline
            if over_time.total_seconds() < 3600:
                return ''.join(['已超时', str(int(over_time.total_seconds() / 60)), '分钟'])
            elif 3600 <= over_time.total_seconds() < 86400:
                return ''.join(['已超时', str(int(over_time.total_seconds() / 3600)), '小时'])
            else:
                return ''.join(['已超时', str(int(over_time.total_seconds() / 86400)), '天'])
        elif self.status == 1:
            over_time = self.done_time - self.deadline
            if over_time.total_seconds() < 3600:
                return ''.join(['超时', str(int(over_time.total_seconds() / 60)), '分钟完成'])
            elif 3600 <= over_time.total_seconds() < 86400:
                return ''.join(['超时', str(int(over_time.total_seconds() / 3600)), '小时完成'])
            else:
                return ''.join(['超时', str(int(over_time.total_seconds() / 86400)), '天完成'])

    def check_liked(self):
        for uid in self.liked.all():
            if str(uid) == session['user_id']:
                return True


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.TIMESTAMP(), server_default=func.now())
    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)

    def username(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user.username

    def __repr__(self):
        return '<Comment: {}>'.format(self.text[:15])


class Likes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), index=True, nullable=False)
    liked_user = db.Column(db.Integer(), db.ForeignKey('user.id'), index=True, nullable=False)

    def i_like(self, task_id):
        task = Task.query.get(task_id)
        if session['user_id'] != str(task.user_id):
            self.user_id = session['user_id']
            self.task_id = task.id
            self.liked_user = task.user_id

    def __repr__(self):
        return '{}'.format(self.user_id)
