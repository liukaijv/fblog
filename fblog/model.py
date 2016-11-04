# coding: utf-8
from datetime import datetime
from flask_login import current_user
from . import db


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    value = db.Column(db.Text)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(32))
    password = db.Column(db.String(64))
    name = db.Column(db.String(32))
    email = db.Column(db.String(128))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.user_name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    sort = db.Column(db.Integer(), default=255)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __unicode__(self):
        return self.name


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    def __unicode__(self):
        return self.name


tags = db.Table('post_tag',
                db.Column('post_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('post.id'))
                )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    excerpt = db.Column(db.Text)
    sort = db.Column(db.Integer(), default=255)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tags, backref='posts', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self):
        self.user_id = current_user.id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __unicode__(self):
        return self.name


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer)
    body = db.Column(db.Text)
    name = db.Column(db.String(32))
    email = db.Column(db.String(128))
    website = db.Column(db.String(64))
    publish = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __unicode__(self):
        return self.name
