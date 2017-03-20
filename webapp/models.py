from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import AnonymousUserMixin, UserMixin
from sqlalchemy.sql import func
from datetime import datetime
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), index=True)
    password = db.Column(db.String(255))
    reg_date = db.Column(db.TIMESTAMP(), server_default=func.now())
    last_login_date = db.Column(db.DateTime())
    tasks = db.relationship(
        'Task',
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

    def count_all(self):
        return Task.query.filter_by(user_id=self.id).all()

    def count_done(self):
        return Task.query.filter_by(user_id=self.id).filter_by(status=1).all()


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), index=True)
    text = db.Column(db.Text())
    create_time = db.Column(db.TIMESTAMP(), server_default=func.now())
    update_time = db.Column(db.DateTime(), onupdate=func.now())
    done_time = db.Column(db.DateTime())
    deadline = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.SmallInteger(), default=0)  # 0 进行中 1 已完成 2 暂停
    public_level = db.Column(db.SmallInteger(), default=0)
    overtime = db.Column(db.SmallInteger(), default=0)  # 任务结束后： 0 未超时 1 超时
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Task: {}|User:{}>'.format(self.title, self.user_id)

    def is_overtime(self):
        if self.deadline < datetime.now():
            return True
        else:
            return False

    CHARSET = 'utf8mb4'