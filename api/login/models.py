from sqlalchemy import func

from api.base.abstract.abstract_base import BaseMethod
from config.config import Config
from config.settings import db


class TokenBlocklist(db.Model, BaseMethod):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False, index=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    refresh = db.Column(db.String, nullable=False, index=True)
    jti_refresh = db.Column(db.String(36), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=func.now(),
        nullable=False,
    )
    expries_at = db.Column(
        db.DateTime,
        default=func.now() + Config.ACCESS_EXPIRES,
        # default=None,
    )
    status = db.Column(db.Boolean, default=True)
    status_refresh = db.Column(db.Boolean, default=True)

    def __init__(self, token, jti, user_id, refresh_token, jti_refresh):
        self.token = token
        self.jti = jti
        self.user_id = user_id
        self.refresh = refresh_token
        self.jti_refresh = jti_refresh
