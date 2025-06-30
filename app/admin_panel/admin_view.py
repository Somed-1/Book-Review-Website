import os

from flask import redirect, url_for, flash, request, current_app
from flask_admin import BaseView, form, AdminIndexView, expose
from wtforms import validators
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_login import current_user

from app.extensions import admin, db
from app.models import *

from config import Config


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login', next=request.url))


class AdminModelView(ModelView):
    """Base ModelView for admin pages requiring admin permissions"""
    
    def is_accessible(self):
        """Ensure the user is logged in and is an admin"""
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):

        """Redirect to login page if user doesn't have access"""
        flash('You need to be an administrator to access this page.', 'error')
        return redirect(url_for('auth.login'))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('auth.login', next=request.url))


class UserAdminView(AdminModelView):
    """Admin view for User model"""

    
    # Don't display the password hash in the list
    column_exclude_list = ['password_hash']
    # Don't include the password hash when creating or editing a User
    form_excluded_columns = ['password_hash', 'reviews', 'created_at', 'updated_at']
    # Display these columns in the list view
    column_list = ['id', 'username', 'email', 'is_active', 'is_admin', 'created_at']
    # Allow searching on these columns
    column_searchable_list = ['username', 'email']
    # Allow filtering on these columns
    column_filters = ['is_active', 'is_admin', 'created_at']
    # Fast-edit columns in list view
    column_editable_list = ['is_active', 'is_admin']
    
    # Fix form rendering issues

    form_create_rules = [
        'username',
        'email',
        'is_active',
        'is_admin'
    ]
    
    form_edit_rules = [

        'username',
        'email',
        'is_active',
        'is_admin'
    ]


class AuthorAdminView(AdminModelView):
    """Admin view for Author model"""
    
    # Display these columns in the list view
    column_list = ['id', 'name', 'birth_date', 'death_date']
    # Allow searching on these columns
    column_searchable_list = ['name']
    # Allow filtering on these columns
    column_filters = ['birth_date', 'death_date']

    
    # Exclude auto-generated timestamps from forms
    form_excluded_columns = ['created_at', 'updated_at', 'books']
    
    # Define form rules to control field order and display
    form_create_rules = [
        'name',
        'biography',
        'birth_date',
        'death_date'
    ]


class CategoryAdminView(AdminModelView):
    """Admin view for Category model"""

    
    # Display these columns in the list view

    column_list = ['id', 'name', 'description']
    # Allow searching on these columns
    column_searchable_list = ['name', 'description']
    
    # Exclude auto-generated timestamps and relationships from forms
    form_excluded_columns = ['created_at', 'updated_at', 'books']
    
    # Define form rules
    form_create_rules = [

        'name',
        'description'
    ]


class BookAdminView(AdminModelView):
    column_list = ('title', 'publisher', 'publication_date', 'average_rating')
    column_searchable_list = ('title', 'isbn')

    form_columns = [
        'title',
        'isbn',
        'description',

        'publication_date',
        'publisher',
        'pages',
        'language',
        'cover_image',
        'authors',
        'categories',
    ]

    # form_overrides = {
    #     'cover_image': form.ImageUploadField
    # }

    form_args = {
        # 'cover_image': {
        #     'label': 'Cover Image',
        #     'base_path': Config.BOOK_COVER_UPLOAD_PATH,
        #     'url_relative_path': Config.BOOK_COVER_UPLOAD_URL,
        #     'allow_overwrite': False,
        #     'thumbnail_size': (100, 100, True)
        # },
        'authors': {
            'label': 'Authors',
            'query_factory': lambda: Author.query.order_by(Author.name),
            'allow_blank': True,
        },
        'categories': {
            'label': 'Categories',
            'query_factory': lambda: Category.query.order_by(Category.name),
            'allow_blank': True,
        },
    }

    def on_form_prefill(self, form, id):
        # Overwrite dynamically if needed
        self.form_extra_fields['cover_image'].base_path = current_app.config['BOOK_COVER_UPLOAD_PATH']
        self.form_extra_fields['cover_image'].url_relative_path = current_app.config['BOOK_COVER_UPLOAD_URL']

    form_extra_fields = {
        'cover_image': form.ImageUploadField(
            label='Book Cover',
            base_path=Config.BOOK_COVER_UPLOAD_PATH,
            url_relative_path=Config.BOOK_COVER_UPLOAD_URL,
            allowed_extensions=('jpg', 'jpeg', 'png', 'gif'),
            max_size=(500, 800, True),
            thumbnail_size=(100, 150, True),
            description='Upload a JPG/PNG cover image'
        )
    }
    # helper methods to fetch config from the app
    def get_upload_path(self):
        return self.admin.app.config['BOOK_COVER_UPLOAD_PATH']

    def get_upload_url(self):
        return self.admin.app.config['BOOK_COVER_UPLOAD_URL']

    # (optional) keep “rules” styling
    form_create_rules = [
        rules.FieldSet(('title', 'isbn', 'description'), 'Core Info'),
        rules.FieldSet(('publication_date', 'publisher', 'pages', 'language'), 'Publishing'),
        rules.FieldSet(('cover_image', 'authors', 'categories'), 'Extras'),
    ]
    form_edit_rules = form_create_rules

    column_formatters = {
        'average_rating': lambda v, c, m, p: f"{m.average_rating:.2f}" if m.average_rating else "No Ratings"
    }


class ReviewAdminView(AdminModelView):
    """Admin view for Review model"""
    
    # Display these columns in the list view
    column_list = ['id', 'rating', 'title', 'created_at']
    # Allow searching on these columns
    column_searchable_list = ['title', 'content']
    # Allow filtering on these columns - simplified filters
    column_filters = ['rating', 'created_at']
    
    # Exclude auto-generated timestamps from forms
    form_excluded_columns = ['created_at', 'updated_at']
    
    # Show relationships in a safe way
    column_formatters = {
        'user': lambda v, c, m, p: m.user.username if m.user else 'Unknown user',
        'book': lambda v, c, m, p: m.book.title if m.book else 'Unknown book'
    }
    
    # Define form rules
    form_create_rules = [
        'user',
        'book',
        'title',
        'content',
        'rating'
    ]
    
    # Add form validation
    form_args = {
        'rating': {
            'validators': [],
            'description': 'Rating from 1 to 5'
        }
    }


def register_admin_views():
    """Register all admin views with the admin interface"""
    admin.add_view(UserAdminView(User, db.session, name='Users'))
    admin.add_view(AuthorAdminView(Author, db.session, name='Authors'))
    admin.add_view(CategoryAdminView(Category, db.session, name='Categories'))
    admin.add_view(BookAdminView(Book, db.session, name='Books'))
    admin.add_view(ReviewAdminView(Review, db.session, name='Reviews'))
