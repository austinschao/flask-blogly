from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

DEFAULT_IMG_URL = '/static/img/dog.jpeg'


def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)


"""Models for Blogly."""

class User(db.Model):
    """ Creating a User """

    __tablename__ = 'users'

    posts = db.relationship('Post', backref = 'user')

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    first_name = db.Column(db.String(50),
                            nullable = False)

    last_name = db.Column(db.String(50),
                            nullable = False)

    image_url = db.Column(db.Text,
                            nullable = True, default = DEFAULT_IMG_URL)


class Post(db.Model):
    """ Creating a Post """

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    title = db.Column(db.String(50),
                        nullable = False)

    content = db.Column(db.Text,
                        nullable = False)

    created_at = db.Column(db.DateTime(timezone = True),
                        default = datetime.datetime.utcnow,
                        nullable = False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))


# class Tag(db.Model):
#     """ Creating a tag """

#     __tablename__ = 'tags'

#     id = db.Column(db.Integer,
#                     primary_key = True,
#                     autoincrement = True)

#     name = db.Column(db.String(50),
#                         nullable = False)

# class PostTag(db.Model):
#     """ Join Table for Post and Tag """

#     __tablename__ = 'posts_tags'

#     post_id = (db.Integer,
#                 db.ForeignKey)