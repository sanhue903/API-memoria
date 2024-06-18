from flask import Blueprint

bp = Blueprint('aules', __name__)

from app.aule import routes