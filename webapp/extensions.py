from flask_login import LoginManager
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

login_manager = LoginManager()
redis_store = FlaskRedis()
db = SQLAlchemy()
alembic = Alembic()


login_manager.login_view = 'login.home'
login_manager.session_protection = 'basic'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    from webapp.models import User
    return User.query.get(user_id)
