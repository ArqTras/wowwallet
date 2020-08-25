from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt
from redis import Redis
from wowstash import config


app = None
db = None
bcrypt = None

def _setup_db(app: Flask):
    global db
    uri = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=config.DB_USER,
        pw=config.DB_PASS,
        url=config.DB_HOST,
        db=config.DB_NAME
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    import wowstash.models
    db.create_all()

def _setup_session(app: Flask):
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_COOKIE_NAME'] = app.config.get('SESSION_COOKIE_NAME', 'wowstash')
    app.config['SESSION_REDIS'] = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT']
    )
    Session(app)

def _setup_bcrypt(app: Flask):
    global bcrypt
    bcrypt = Bcrypt(app)

def create_app():
    global app
    global db
    app = Flask(__name__)
    app.config.from_envvar('FLASK_SECRETS')
    app.secret_key = app.config['SECRET_KEY']

    # Setup backends
    _setup_db(app)
    _setup_session(app)
    _setup_bcrypt(app)

    # Routes
    from wowstash.blueprints.authentication import authentication_bp
    from wowstash.blueprints.account import account_bp
    from wowstash.blueprints.meta import meta_bp
    app.register_blueprint(meta_bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(account_bp)

    app.app_context().push()
    return app
