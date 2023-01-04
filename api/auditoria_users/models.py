from sqlalchemy import func

from config.settings import db


class AuditoriaUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(
        db.DateTime,
        default=func.now(),
        nullable=False,
    )
    auxiliar = db.Column(db.String(50), nullable=True, default=None)
    date_end = db.Column(
        db.DateTime,
        nullable=True,
    )
    duracion = db.Column(db.Integer, nullable=True)
    estado = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, auxiliar, user_id, duracion=None):
        self.auxiliar = auxiliar
        self.duracion = duracion
        self.user_id = user_id
