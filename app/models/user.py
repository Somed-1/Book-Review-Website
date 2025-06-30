from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(2048), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))
