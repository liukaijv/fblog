# coding: utf-8
from flask_script import Manager, Server, prompt_bool
from werkzeug.security import generate_password_hash

from fblog.model import db
from fblog.views import app

manager = Manager(app)
manager.add_command('runserver', Server('0.0.0.0', port=5000))
config = app.config


@manager.command
def create_db():
    db.create_all()


@manager.option('-u', '--name', dest='name', default='admin')
@manager.option('-p', '--password', dest='password', default='admin')
def create_user(name, password):
    from fblog.model import User
    user = User(name, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()


@manager.command
def drop_db():
    if prompt_bool('Are you sure? You will lose all your data!'):
        db.drop_all()


if __name__ == '__main__':
    manager.run()
