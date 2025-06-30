import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    USER: str = os.environ["SQL_USER"]
    PASSWORD: str = os.environ["SQL_PASSWORD"]
    DB_NAME: str = os.environ["SQL_NAME"]
    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+mysqldb://{USER}:{PASSWORD}@db/{DB_NAME}"
    )

    SECRET_TOKEN: str = os.environ["SECRET_TOKEN"]
    SECRET_KEY: str = os.environ["SECRET_TOKEN"]
    FLASK_ADMIN_SWATCH: str = "cerulean"
    BOOK_COVER_UPLOAD_PATH = os.path.join(basedir, 'app', 'static', 'uploads', 'covers')
    BOOK_COVER_UPLOAD_URL  = '/static/uploads/covers/'
