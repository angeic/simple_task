from webapp.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import or_, and_
from datetime import datetime
from flask import session


follows = db.Table('follows',
                   db.Column('user_id', db.ForeignKey('user.id')),
                   db.Column('follow_id', db.ForeignKey('user.id'))
                   )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    bio = db.Column(db.String(100))
    gender = db.Column(db.SmallInteger(), default=0)  # 1 男 2 女 0 未填写
    email = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(255))
    reg_date = db.Column(db.TIMESTAMP(), server_default=func.now())
    last_login_date = db.Column(db.DateTime())
    wb_uid = db.Column(db.String(20))
    avatar = db.Column(db.String(500))
    tasks = db.relationship(
        'Task',
        backref='user',
        lazy='dynamic'
    )

    comments = db.relationship(
        'Comment',
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

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    # 检查是否关注
    def check_following(self, user_id):
        if User.query.get(user_id) in self.following.all():
            return True

    # 互相关注的好友
    def friends(self):
        return list(set(self.following.all()) & set(self.follower.all()))

    # 添加关注
    def add_following(self, user_id):
        self.following.append(User.query.get(user_id))
        db.session.add(self)
        db.session.commit()

    # 取消关注
    def cancel_following(self, user_id):
        self.following.remove(User.query.get(user_id))
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def count_task(self):
        return '创建了{}个任务，完成了{}个'.format(len(self.tasks.all()), len(self.tasks.filter_by(status=1).all()))

    def unfinish_task(self):
        return len(self.tasks.all()) - len(self.tasks.filter_by(status=1).all())

    # 从微博注册用户
    def wb_reg(self, wb_uid):
        if not User.query.filter_by(wb_uid=wb_uid).first():
            self.wb_uid = wb_uid

    # 查询当前登录用户关注的人中是否有人关注了页面显示的用户
    def relation(self):
        if current_user.username != self.username:
            return list(set(current_user.following.all()) & set(self.follower.all()))

    def gender_text(self):
        return '他'if self.gender else '她'

    # 取用户头像，为空则取默认头像
    def get_avatar(self):
        if self.avatar:
            return '/static/images/'+self.avatar
        else:
            if self.gender == 0:
                return '/static/images/0.png'
            else:
                return '/static/images/1.png'

    # 圈子内容
    def circle_task(self):
        query_1 = and_(Task.user_id.in_([user.id for user in self.following.all()]), Task.public_level == '3') if self.following.all() else None  # 关注的
        query_2 = and_(Task.user_id.in_([user.id for user in self.friends()]), Task.public_level == '2') if self.friends() else None  # 互相关注的
        return Task.query.filter(or_(Task.user_id == self.id, query_1, query_2)
        ).order_by(Task.create_time.desc()).all()


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False, index=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text())
    create_time = db.Column(db.TIMESTAMP(), server_default=func.now())
    update_time = db.Column(db.DateTime(), onupdate=func.now())
    done_time = db.Column(db.DateTime())
    deadline = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.SmallInteger(), default=0)  # 0：进行中 1：已完成 2：暂停 9：删除
    public_level = db.Column(db.SmallInteger(), default=3, index=True)  # 1：仅自己可见   2：我关注的人可见   3：所有人可见
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

    # 判断任务是否超时
    def is_overtime(self):
        if self.status == 0 and self.deadline > datetime.now():
            return False
        elif self.status == 1 and self.overtime == 0:
            return False
        else:
            return True

    # 超时时间
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
        else:
            pass

    # 给任务点赞的所有user_id
    def liked_user(self):
        return list(u.user_id for u in self.liked.all())

    # 判断是否已点赞
    def check_liked(self):
        if current_user.id in self.liked_user():
            return True

    # 距离超时一小时
    def one_hour_deadline(self):
        the_time = self.deadline - datetime.now()
        if 0 < the_time.total_seconds() < 3600:
            return True

    # 判断当前用户是否有权限查看当前task
    def task_auth(self):
        task_user = User.query.get(self.user_id)
        if current_user.id == self.user_id or self.public_level == 3 or (current_user in task_user.follower.all() and self.public_level == 2):
            return True
        else:
            return False


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.TIMESTAMP(), server_default=func.now())
    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)

    def __repr__(self):
        return '<Comment: {}>'.format(self.text[:15])


class Likes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), index=True, nullable=False)
    liked_user = db.Column(db.Integer(), db.ForeignKey('user.id'), index=True, nullable=False)

    def i_like(self, task_id):
        task = Task.query.get(task_id)
        self.user_id = session['user_id']
        self.task_id = task.id
        self.liked_user = task.user_id

    def __repr__(self):
        return '{}'.format(self.user_id)
