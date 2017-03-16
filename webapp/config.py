

class Config:
    pass


class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://simple_dev:simple_dev@192.168.5.7:3306/simple_task_test"
    SECRET_KEY = 'hard to guess string abc heheda'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
