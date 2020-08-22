from flask import Flask, jsonify, request, make_response, render_template, session, redirect, url_for, escape
from flask_session import Session
from datetime import timedelta, datetime
from redis import Redis
from wowstash.library.jsonrpc import daemon
from wowstash.library.info import info
from wowstash.library.db import Database
from wowstash import config
# from wowstash.blueprints.account import account_bp
# from wowstash.blueprints.authentication import authentication_bp

# Setup app
app = Flask(__name__)
app.config.from_envvar('FLASK_SECRETS')
app.secret_key = app.config['SECRET_KEY']

# Setup sessions
app.config['SESSION_REDIS'] = Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT']
)
sess = Session()
sess.init_app(app)

# app.register_blueprint(account_bp)
# app.register_blueprint(authentication_bp)

@app.route('/')
def index():
    return render_template('home.html', node=daemon.info(), info=info.get_info())

@app.route('/health')
def health():
    return make_response(jsonify({
        'cache': info.redis.ping(),
        'db': Database().connected
    }), 200)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': 'Page not found'
    }), 404)

@app.cli.command('eviscerate')
def eviscerate():
    print('Eviscerate the proletariat')

if __name__ == '__main__':
    app.run()
