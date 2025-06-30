from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.routes.review import bp
from app.extensions import db
from app.forms.review import ReviewForm
from app.models import Book, Review

@bp.route('/review/<int:book_id>', methods=['GET', 'POST'])
@login_required
def add_review(book_id):
    """
    Route to add a new review for a book.
    GET: Display the review form
    POST: Process the submitted review
    """
    # Get the book or return 404 if not found
    book = Book.query.get_or_404(book_id)
    
    # Check if user has already reviewed this book
    existing_review = Review.query.filter_by(
        user_id=current_user.id, 
        book_id=book_id
    ).first()
    
    # Initialize the form
    form = ReviewForm()
    form.book_id.data = book_id
    
    if request.method == 'GET':
        # Render the template with the form
        return render_template(
            'review/review.html',  # Adjust path as needed
            form=form,
            book=book,
            existing_review=existing_review
        )
    
    if form.validate_on_submit():
        try:
            # Create new review
            new_review = Review(
                user_id=current_user.id,
                book_id=book_id,
                title=form.title.data.strip() if form.title.data else None,
                content=form.content.data.strip() if form.content.data else None,
                rating=float(form.rating.data)
            )
            
            # Add to database
            db.session.add(new_review)
            db.session.commit()
            
            flash('Your review has been added successfully!', 'success')
            return redirect(url_for('book_page.book_page', id=book_id))
            
        except Exception as e:
            # Handle database errors (like unique constraint violation)
            db.session.rollback()
            flash('An error occurred while saving your review. Please try again.', 'error')
            
    # If form validation fails, re-render with errors
    return render_template(
        'review/review.html',
        form=form,
        book=book,
        existing_review=existing_review
    )
