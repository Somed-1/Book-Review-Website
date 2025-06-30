from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect destination when login required
login_manager.login_message = 'Please log in to access this page.'

admin = Admin(name='Book Review Admin', template_mode='bootstrap4')
