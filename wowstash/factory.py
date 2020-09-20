from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from redis import Redis
from datetime import datetime
from wowstash import config


app = None
db = None
bcrypt = None

def _setup_db(app: Flask):
    global db
    uri = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
        user=config.DB_USER,
        pw=config.DB_PASS,
        host=config.DB_HOST,
        port=config.DB_PORT,
        db=config.DB_NAME
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    import wowstash.models
    db.create_all()

def _setup_session(app: Flask):
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
    global bcrypt
    global login_manager
    app = Flask(__name__)
    app.config.from_envvar('FLASK_SECRETS')
    app.secret_key = app.config['SECRET_KEY']

    # Setup backends
    _setup_db(app)
    _setup_session(app)
    _setup_bcrypt(app)
    CSRFProtect(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from wowstash.models import User
        user = User.query.get(user_id)
        return user

    # template filters
    @app.template_filter('datestamp')
    def datestamp(s):
        d = datetime.fromtimestamp(s)
        return d.strftime('%Y-%m-%d %H:%M:%S')

    @app.template_filter('from_atomic')
    def from_atomic(a):
        from wowstash.library.jsonrpc import from_atomic
        return from_atomic(a)

    # commands
    @app.cli.command('create_wallets')
    def create_wallets():
        import subprocess
        from os import makedirs, path
        from moneropy import account
        from wowstash import config
        from wowstash.factory import db
        from wowstash.models import User
        from wowstash.library.jsonrpc import daemon

        if not path.isdir(config.WALLET_DIR):
            makedirs(config.WALLET_DIR)

        wallets_to_create = User.query.filter_by(wallet_created=False)
        if wallets_to_create:
            for u in wallets_to_create:
                print(f'Creating wallet for user {u}')
                seed, sk, vk, addr = account.gen_new_wallet()
                command = f"""wownero-wallet-cli \
                --generate-new-wallet {config.WALLET_DIR}/{u.id}.wallet \
                --restore-height {daemon.info()['height']} \
                --password {u.wallet_password} \
                --mnemonic-language English \
                --daemon-address {config.DAEMON_PROTO}://{config.DAEMON_HOST}:{config.DAEMON_PORT} \
                --daemon-login {config.DAEMON_USER}:{config.DAEMON_PASS} \
                --command version
                """
                proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                proc.communicate()
                if proc.returncode == 0:
                    print(f'Successfully created wallet for {u}!')
                    u.wallet_created = True
                    db.session.commit()
                else:
                    print(f'Failed to create wallet for {u}.')

    @app.cli.command('refresh_wallets')
    def refresh_wallets():
        import subprocess
        from os import kill
        from moneropy import account
        from wowstash import config
        from wowstash.factory import db
        from wowstash.models import User
        from wowstash.library.jsonrpc import daemon

        users = User.query.all()
        for u in users:
            print(f'Refreshing wallet for {u}')

            if u.wallet_pid is None:
                break

            # first check if the pid is still there
            try:
                kill(u.wallet_pid, 0)
            except OSError:
                print('pid does not exist')
                u.wallet_connected = False
                u.wallet_pid = None
                u.wallet_connect_date = None
                u.wallet_port = None
                db.session.commit()

            # then check if the user session is still active
            if u.is_active is False:
                print('user session inactive')
                kill(u.wallet_pid, 9)
                u.wallet_connected = False
                u.wallet_pid = None
                u.wallet_connect_date = None
                u.wallet_port = None
                db.session.commit()

    # Routes
    from wowstash.blueprints.auth import auth_bp
    from wowstash.blueprints.wallet import wallet_bp
    from wowstash.blueprints.meta import meta_bp
    app.register_blueprint(meta_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(wallet_bp)

    app.app_context().push()
    return app
