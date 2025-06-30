from datetime import datetime
from app.extensions import db

from sqlalchemy import UniqueConstraint

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    rating = db.Column(db.Float, nullable=False)  # e.g., 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='reviews')
    book = db.relationship('Book', back_populates='reviews')
    
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='uix_user_book'),  # This line prevents multiple reviews
        {'sqlite_autoincrement': True},
    )
    
    def __repr__(self):
        return f'<Review {self.id} by {self.user.username} for {self.book.title}>'
