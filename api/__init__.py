from api.auditoria_users.views import audit
from api.categorias.views import categorias
from api.login.views import auth
from api.user.views import user


def register_views(app):
    app.register_blueprint(user)
    app.register_blueprint(categorias)
    app.register_blueprint(auth)
    app.register_blueprint(audit)
