from flask_login import LoginManager

login_manager = LoginManager()


login_manager.login_view = 'login.index'
login_manager.session_protection = 'basic'


@login_manager.user_loader
def load_user(user_id):
    from webapp.models import User
    return User.query.get(user_id)
