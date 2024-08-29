from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(50), unique=True)
    # SECURITY NOTE: Don't actually store passwords like this in a real system!
    password = db.mapped_column(db.String(80))

    def __str__(self):
        return self.username


class BlogPost(db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(100), nullable=False)
    content = db.mapped_column(db.Text, nullable=False)
    created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
    author_id = db.mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    author = db.relationship('User', backref=db.backref('blog_posts', lazy=True))
    # backref: A back reference that will add a virtual column to the User model.
    # This part essentially creates an automatic attribute (blog_posts) on instances of the User model.
    # The blog_posts attribute will provide access to all BlogPost instances related to a particular user,
    # facilitating the reverse lookup from User to BlogPost.

    # lazy=True: This option controls how the related items are loaded.
    # Setting lazy=True (equivalent to lazy='select') means that the related items (blog posts in this case)
    # are loaded on demand. The SQL query to retrieve these items is not run until you access the
    # blog_posts attribute, which helps improve performance by not loading related data until it's explicitly needed.

    def __str__(self):
        return f'"{self.title}" by {self.author.username} ({self.created_at:%Y-%m-%d})'

    @staticmethod
    def get_post_lengths():
        # An example of how to use raw SQL inside a model
        sql = text("SELECT length(title) + length(content) FROM blog_post")
        return db.session.execute(sql).scalars().all()  # Returns just the integers
