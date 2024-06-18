from flask import Blueprint

bp = Blueprint('score', __name__)

from app.score import routes