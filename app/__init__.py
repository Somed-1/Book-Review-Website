from flask import Flask, render_template
from flask_login import current_user, login_required
from flask_migrate import Migrate

from app.extensions import db, login_manager, admin
from config import Config

from app.admin_panel.admin_view import register_admin_views, MyAdminIndexView

from app.models import User, Book, Review, Author, Category


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)

    admin.init_app(app, index_view=MyAdminIndexView())

    register_admin_views()

    from app.routes.auth import bp as auth_bp
    from app.routes.home import bp as home_bp
    from app.routes.book import bp as book_bp
    from app.routes.user import bp as user_bp
    from app.routes.review import bp as review_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(review_bp)

    @app.route("/test")
    def test_page():
        return render_template("test.html", user=current_user)

    return app
