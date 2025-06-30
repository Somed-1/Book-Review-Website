from flask import Blueprint

bp = Blueprint("book_page", __name__, template_folder="../templates/book")

from app.routes.book import routes
