import os.path
import configparser

BASE_DIR = os.path.abspath('.')
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.ini'), encoding='utf8')


def get_config(section, option, default=None):
    try:
        return config.get(section, option)
    except (configparser.NoOptionError, configparser.NoSectionError):
        return default


class Config:
    DEBUG = True
    SECRET_KEY = get_config('config', 'secret_key')
    WTF_CSRF_ENABLED = True

    ALEMBIC_CONTEXT = {'compare_type': True}

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{pw}@{host}:{port}/{db}".format(
        user=get_config('database', 'user'),
        pw=get_config('database', 'pass'),
        host=get_config('database', 'host'),
        port=get_config('database', 'port'),
        db=get_config('database', 'name')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Celery 配置
    CELERY_BROKER_URL = get_config('celery', 'uri')
    CELERY_RESULT_BACKEND = get_config('celery', 'uri')

    # 微博接口配置
    WB_APP_KEY = get_config('weibo', 'app_key')
    WB_APP_SECRET = get_config('weibo', 'app_secret')
