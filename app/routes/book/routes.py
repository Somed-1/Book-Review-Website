from flask import render_template
from sqlalchemy import desc
from app.routes.book import bp
from app.models import Book, Review, Author, Category

@bp.route("/book/<int:id>")
def book_page(id):
    # Get the book by ID or return 404 if not found
    book = Book.query.get_or_404(id)
    
    # Get reviews ordered by most recent first
    reviews = Review.query.filter_by(book_id=id).order_by(desc(Review.created_at)).all()
    
    # Update the book object with the reviews for template access
    book.reviews = reviews
    
    # Optional: Get related books (same authors or categories)
    related_books = []
    if book.authors:
        # Get other books by the same authors (limit to 4)
        author_ids = [author.id for author in book.authors]
        related_books = Book.query.join(Book.authors).filter(
            Author.id.in_(author_ids),
            Book.id != id
        ).distinct().limit(4).all()
    
    # If no books by same authors, get books from same categories
    if not related_books and book.categories:
        category_ids = [category.id for category in book.categories]
        related_books = Book.query.join(Book.categories).filter(
            Category.id.in_(category_ids),
            Book.id != id
        ).distinct().limit(4).all()
    
    return render_template("book/book.html", 
                         book=book, 
                         reviews=reviews,
                         related_books=related_books)

