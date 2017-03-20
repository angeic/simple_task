from os import path


class Config:
    pass


class DevConfig:
    basedir = path.abspath(path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://simple_dev:simple_dev@192.168.5.7:3306/simple_task_test?charset=utf8mb4"
    SECRET_KEY = 'hard to guess string abc heheda'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
