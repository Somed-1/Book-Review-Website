from datetime import datetime
from app.extensions import db
from app.models.association_tables import book_author, book_category


class Book(db.Model):
    __tablename__ = 'books'
    

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True, index=True)
    publication_date = db.Column(db.DateTime)
    publisher = db.Column(db.String(128))
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(256))  # URL or path to the image
    pages = db.Column(db.Integer)
    language = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    # Relationships
    authors = db.relationship('Author', secondary=book_author, back_populates='books')
    categories = db.relationship('Category', secondary=book_category, back_populates='books')
    reviews = db.relationship('Review', back_populates='book', cascade='all, delete-orphan')
    
    @property
    def average_rating(self):

        if not self.reviews:

            return None
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    def __repr__(self):
        return f'<Book {self.title}>'
