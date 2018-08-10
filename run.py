from webapp import create_app
from webapp.config import Config
from webapp.extensions import alembic

app = create_app(Config)
alembic.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
