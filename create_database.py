from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from manage import app
from sqlalchemy.sql import func
from flask_login import UserMixin
import time
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    bio = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), index=True)
    password = db.Column(db.String(255))
    reg_date = db.Column(db.TIMESTAMP(), server_default=func.now())
    last_login_date = db.Column(db.DateTime())
    tasks = db.relationship(
        'Task',
        backref='user',
        lazy='dynamic'
    )

    follow_list = db.relationship(
        'Follow',
        backref='user',
        lazy='dynamic'
    )

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


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), index=True)
    text = db.Column(db.Text())
    create_time = db.Column(db.TIMESTAMP(), server_default=func.now())
    update_time = db.Column(db.DateTime(), onupdate=func.now())
    done_time = db.Column(db.DateTime())
    deadline = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.SmallInteger(), default=0)  # 0：进行中 1：已完成 2：暂停
    public_level = db.Column(db.SmallInteger(), default=0)  # 1：仅自己可见   2：互相关注的好友可见   3：所有人可见
    overtime = db.Column(db.SmallInteger(), default=0)  # 任务结束后： 0：未超时 1：超时
    comment_allowed = db.Column(db.SmallInteger(), default=1)  # 0：禁止评论并隐藏所有评论内容 1：允许评论
    comments = db.relationship(
        'Comment',
        backref='task',
        lazy='dynamic'
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Task: {}|User:{}>'.format(self.title, self.user_id)

    def is_overtime(self):
        if self.status == 0 and self.deadline < datetime.now() or self.overtime == 1:
            return True

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

    def count_comments(self):
        return Comment.query.filter_by(task_id=self.id).all()


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


class Follow(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False, index=True)
    follow_id = db.Column(db.Integer(), nullable=False)
    is_friend = db.Column(db.SmallInteger(), default=0, index=True)  # 0：非互相关注 1：互相关注

    def __repr__(self):
        return '<Follow {},is_friend:{}>'.format(self.follow_id, self.is_friend)

    def __init__(self, user_id):
        self.user_id = user_id

    def check_follow(self, follow_id):
        return Follow.query.filter(Follow.user_id == self.user_id, Follow.follow_id == follow_id).first()

    def check_friend(self, follow_id):
        return Follow.query.filter(Follow.user_id == follow_id, Follow.follow_id == self.user_id).first()

    def set_follow(self, follow_id):
        self.follow_id = follow_id
        if self.check_friend(follow_id):
            self.is_friend = 1
            Follow.query.filter(Follow.user_id == follow_id, Follow.follow_id == self.user_id).update({
                'is_friend': 1
            })
            db.session.commit()

    def cancel_follow(self, follow_id):
        if self.check_friend(follow_id):
            Follow.query.filter(Follow.user_id == follow_id, Follow.follow_id == self.user_id).update({
                'is_friend': 0
            })
            #db.session.commit()
        cancel = Follow.query.filter(Follow.user_id == self.user_id, Follow.follow_id == follow_id).first()
        db.session.delete(cancel)
        #db.session.commit()