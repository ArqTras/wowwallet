

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': 'Page not found'
    }), 404)

@app.cli.command('initdb')
def initdb():
    from wowstash.models import *
    db.create_all()
