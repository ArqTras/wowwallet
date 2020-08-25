from flask import request, render_template, session, redirect, url_for, make_response, jsonify
from wowstash.blueprints.meta import meta_bp
from wowstash.library.jsonrpc import daemon
from wowstash.library.info import info
from wowstash.library.db import Database


@meta_bp.route('/')
def index():
    return render_template('index.html', node=daemon.info(), info=info.get_info())

@meta_bp.route('/health')
def health():
    return make_response(jsonify({
        'cache': info.redis.ping(),
        'db': Database().connected
    }), 200)
 
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({
#         'error': 'Page not found'
#     }), 404)
