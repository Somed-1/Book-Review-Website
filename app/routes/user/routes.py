from flask import render_template

from sqlalchemy import func, desc

from app.routes.user import bp
from app.extensions import db
from app.models import *

@bp.route("/profile/<int:id>")
def home(id):
    return render_template("/user/profile.html")
