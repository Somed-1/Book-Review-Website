from flask import Blueprint

bp = Blueprint("review_page", __name__, template_folder="../templates/review")

from app.routes.review import routes
