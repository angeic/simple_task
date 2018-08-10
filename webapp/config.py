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

    WBAppKey = get_config('weibo', 'app_key')
    WBAppSecret = get_config('weibo', 'app_secret')
