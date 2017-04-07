from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField, DateTimeField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, length, EqualTo, Optional
from .models import User, db, Task
from flask import session, g, flash
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired('账号未填写')])
    password = PasswordField('密码', validators=[DataRequired('密码未填写')])
    remember = BooleanField('记住我')
    login_submit = SubmitField('登录')

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append(
                '用户名或密码错误'
            )
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append(
                '用户名或密码错误'
            )
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired('必须填写账号'), length(max=20, message='长度不可以超过20')])
    email = StringField('Email', validators=[DataRequired('必须填写Email'), length(max=50, message='长度不能超过50'), Email(message='Email格式不正确')])
    password = PasswordField('密码', validators=[DataRequired(), length(8, 30, '密码长度必须在8-30位'), EqualTo('password_verify', '两次输入的密码不一致')])
    password_verify = PasswordField('确认密码', validators=[DataRequired(), length(8, 30, '密码长度必须在8-30位')])
    register_submit = SubmitField('注册')

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(
                '该用户名已存在，请更换其他用户名'
            )
            return False

        email = User.query.filter_by(email=self.email.data).first()
        if email:
            self.email.errors.append(
                'Email地址已存在，请更换其他Email地址'
            )
            return False

        user_register = User(self.username.data)
        user_register.set_password(self.password.data)
        user_register.email = self.email.data
        db.session.add(user_register)
        db.session.commit()

        return True


class TaskForm(FlaskForm):
    title = StringField('主题', validators=[DataRequired('未填写主题'), length(max=100, message='长度不能超过100')])
    text = TextAreaField('内容', validators=[DataRequired('未填写内容'), length(max=1000, message='长度不能超过1000')])
    deadline = DateTimeField('到期时间', validators=[DataRequired('未设置到期时间')])
    public_level = RadioField('公开级别', choices=[('1', '仅自己可见'), ('2', '好友可见'), ('3', '所有人可见')])
    comment_allowed = BooleanField('允许评论', default=True)
    submit = SubmitField('提交')

    def validate(self):
        check_validate = super(TaskForm, self).validate()

        if not check_validate:
            return False

        if self.deadline.data < datetime.now():
            self.deadline.errors.append(
                '到期时间不能小于当前时间'
            )
            return False

        return True


class EditForm(FlaskForm):
    title = StringField('主题', validators=[DataRequired('未填写主题'), length(max=100, message='长度不能超过100')])
    text = TextAreaField('内容', validators=[DataRequired('未填写内容'), length(max=1000, message='长度不能超过1000')])
    deadline = DateTimeField('到期时间', validators=[DataRequired('未设置到期时间')])
    public_level = RadioField('公开级别', choices=[('1', '仅自己可见'), ('2', '互相关注的好友可见'), ('3', '所有人可见')])
    comment_allowed = BooleanField('允许评论')
    submit = SubmitField('修改')


class CommentForm(FlaskForm):
    text = TextAreaField('评论内容', validators=[DataRequired('未填写内容'), length(max=1000, message='长度不能超过1000')])
    submit = SubmitField('提交')


