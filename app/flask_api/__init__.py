from flask import Blueprint

bp = Blueprint('flask_api', __name__)

from app.flask_api import routes