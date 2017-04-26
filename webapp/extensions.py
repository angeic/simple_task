from flask_login import LoginManager

login_manager = LoginManager()


login_manager.login_view = 'login.home'
login_manager.session_protection = 'basic'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    from webapp.models import User
    return User.query.get(user_id)
