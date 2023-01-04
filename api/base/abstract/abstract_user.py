from api.base.abstract.abstract_base import ModelBase, db


class AbstractUser(ModelBase):
    __abstract__ = True
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)

