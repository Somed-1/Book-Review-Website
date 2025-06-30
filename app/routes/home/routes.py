from flask import render_template, redirect, url_for, flash, request

from sqlalchemy import or_, and_, desc, asc, func

from app.routes.home import bp
from app.extensions import db
from app.models import *

from app.models import Book, Author, Category, Review

@bp.route("/")
def home():
    popular_categories = (
        db.session.query(Category)
        .join(book_category, Category.id == book_category.c.category_id)
        .group_by(Category.id)
        .order_by(func.count(book_category.c.book_id).desc())
        .limit(4)
        .all()
    )
    featured_books = (
        db.session.query(Book, func.avg(Review.rating).label('avg_rating'))
        .join(Review)
        .group_by(Book.id)
        .order_by(desc('avg_rating'))
        .limit(4)
        .all()
    )
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(4).all()
    books_with_ratings = []
    for book, avg in featured_books:
        book.avg_rating = avg  # override the @property just for this context
        books_with_ratings.append(book)
    return render_template("index.html", stats=Stats(), popular_categories=popular_categories, featured_books=books_with_ratings, recent_reviews=recent_reviews)

class Stats:

    def __init__(self) -> None:
        self.total_books = Book.query.count()
        self.total_authors = Author.query.count()
        self.total_reviews = Review.query.count()
        self.total_users = User.query.count()

@bp.route("/search")
def search():
    # Get search parameters
    query = request.args.get('q', '').strip()
    title = request.args.get('title', '').strip()
    author = request.args.get('author', '').strip()
    category_id = request.args.get('category', '').strip()
    publisher = request.args.get('publisher', '').strip()
    language = request.args.get('language', '').strip()
    min_rating = request.args.get('min_rating', '').strip()
    sort_by = request.args.get('sort', 'relevance')
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of books per page
    
    # Get all categories for the filter dropdown
    categories = Category.query.order_by(Category.name).all()
    
    # Start building the query
    books_query = Book.query
    
    # Apply filters
    filters = []
    
    # General search query (searches title, description, and author names)
    if query:
        filters.append(
            or_(
                Book.title.ilike(f'%{query}%'),
                Book.description.ilike(f'%{query}%'),
                Book.authors.any(Author.name.ilike(f'%{query}%'))
            )
        )
    
    # Specific field filters
    if title:
        filters.append(Book.title.ilike(f'%{title}%'))
    
    if author:
        filters.append(Book.authors.any(Author.name.ilike(f'%{author}%')))
    
    if category_id:
        try:
            category_id = int(category_id)
            filters.append(Book.categories.any(Category.id == category_id))
        except ValueError:
            pass
    
    if publisher:
        filters.append(Book.publisher.ilike(f'%{publisher}%'))
    
    if language:
        filters.append(Book.language.ilike(f'%{language}%'))
    
    # Apply all filters
    if filters:
        books_query = books_query.filter(and_(*filters))
    
    # Apply minimum rating filter
    if min_rating:
        try:
            min_rating_value = float(min_rating)
            # Subquery to calculate average rating for each book
            rating_subquery = db.session.query(
                Review.book_id,
                db.func.avg(Review.rating).label('avg_rating')
            ).group_by(Review.book_id).subquery()
            
            books_query = books_query.join(
                rating_subquery, Book.id == rating_subquery.c.book_id
            ).filter(rating_subquery.c.avg_rating >= min_rating_value)
        except ValueError:
            pass
    
    # Apply sorting
    if sort_by == 'title':
        books_query = books_query.order_by(asc(Book.title))
    elif sort_by == 'rating':
        # Order by average rating (highest first)
        rating_subquery = db.session.query(
            Review.book_id,
            db.func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.book_id).subquery()
        
        books_query = books_query.outerjoin(
            rating_subquery, Book.id == rating_subquery.c.book_id
        ).order_by(desc(rating_subquery.c.avg_rating))
    elif sort_by == 'newest':
        books_query = books_query.order_by(desc(Book.publication_date))
    elif sort_by == 'oldest':
        books_query = books_query.order_by(asc(Book.publication_date))
    else:  # relevance (default)
        if query:
            # Simple relevance: exact title matches first, then partial matches
            books_query = books_query.order_by(
                Book.title.ilike(f'{query}%').desc(),
                Book.title.ilike(f'%{query}%').desc(),
                Book.created_at.desc()
            )
        else:
            books_query = books_query.order_by(desc(Book.created_at))
    
    # Paginate results
    books = books_query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template(
        "search.html",  # Adjust path based on your template structure
        books=books,
        query=query,
        categories=categories,
        request=request
    )
