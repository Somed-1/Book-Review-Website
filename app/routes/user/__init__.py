from flask import Blueprint

bp = Blueprint("profile", __name__, template_folder="../templates/user")

from app.routes.user import routes
