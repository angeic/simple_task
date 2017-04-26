from flask_script import Manager, Server
from webapp import create_app
from webapp.config import Config
from webapp.models import db, User, Task, Comment, Likes

app = create_app(Config)

manager = Manager(app)
manager.add_command('server', Server())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, user=User, task=Task, comment=Comment, likes=Likes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
