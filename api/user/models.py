from api.base.abstract.abstract_base import BaseMethod
from api.base.abstract.abstract_user import AbstractUser, db


class User(AbstractUser):
    agente = db.Column(db.String(10), unique=False, nullable=True)
    extension = db.Column(db.String(10), unique=False, nullable=True)
    jwt = db.relationship('TokenBlocklist', backref='user', lazy='dynamic')

    def __init__(self, username, password, first_name, last_name, email, agente=None, extension=None):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.agente = agente
        self.extension = extension

    def toJSON(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
