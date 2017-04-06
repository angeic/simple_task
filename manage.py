from flask_script import Manager, Server
from webapp import create_app
from webapp.config import DevConfig
from webapp.models import db, User, Task, Comment

app = create_app(DevConfig)

manager = Manager(app)
manager.add_command('server', Server())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, user=User, task=Task, comment=Comment)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
