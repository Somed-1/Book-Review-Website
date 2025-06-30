from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import TextArea

def coerce_rating(value):
    """Custom coercion function that handles empty strings"""
    if value == '' or value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

class ReviewForm(FlaskForm):
    # Hidden field for book_id (usually passed from the book detail page)
    book_id = HiddenField('Book ID', validators=[DataRequired()])
    
    # Review title (optional)
    title = StringField(
        'Review Title',
        validators=[
            Optional(),
            Length(max=128, message='Title must be less than 128 characters')
        ],
        render_kw={'placeholder': 'Enter a title for your review (optional)'}
    )
    
    # Review content
    content = TextAreaField(
        'Review Content',
        validators=[
            Optional(),
            Length(max=5000, message='Review content must be less than 5000 characters')
        ],
        widget=TextArea(),
        render_kw={
            'placeholder': 'Share your thoughts about this book...',
            'rows': 6,
            'class': 'form-control'
        }
    )
    
    # Rating field (1-5 stars) - With custom coercion
    rating = SelectField(
        'Rating',
        choices=[
            ('', 'Select a rating'),
            ('1', '1 Star - Poor'),
            ('2', '2 Stars - Fair'),
            ('3', '3 Stars - Good'),
            ('4', '4 Stars - Very Good'),
            ('5', '5 Stars - Excellent')
        ],
        validators=[
            DataRequired(message='Please select a rating')
        ],
        coerce=coerce_rating
    )
