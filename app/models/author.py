from datetime import datetime
from app.extensions import db
from app.models.association_tables import book_author


class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)

    biography = db.Column(db.Text)
    birth_date = db.Column(db.DateTime)
    death_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    books = db.relationship('Book', secondary=book_author, back_populates='authors')

    
    def __repr__(self):

        return f'<Author {self.name}>'
