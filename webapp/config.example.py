from os import path


class Config:
    pass


class DevConfig:
    basedir = path.abspath(path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 1
    SECRET_KEY = 1
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WBAppKey = 1
    WBAppSecret = 1
