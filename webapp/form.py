from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, length, EqualTo
from .models import User, db


class LoginForm(FlaskForm):
    username = StringField('账号',validators=[DataRequired('账号未填写')])
    password = PasswordField('密码',validators=[DataRequired('密码未填写')])
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
    username = StringField('账号', validators=[DataRequired('用户名为必填'), length(max=20, message='长度不可以超过20')])
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

        user_register = User(self.username.data)
        user_register.set_password(self.password.data)
        db.session.add(user_register)
        db.session.commit()

        return True