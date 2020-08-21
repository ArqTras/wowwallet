from flask import Blueprint

authentication_bp = Blueprint("authentication", __name__)

from . import routes
