from config.settings import db


class BaseMethod:

    def save(self):
        try:
            db.session.add(self)
        except Exception as e:
            print("Exception", str(e))
            db.session.rollback()
            raise Exception("Erro al guardar los datos")
        else:
            db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
        except Exception as e:
            db.session.rollback()
            raise Exception("Error al eliminar los datos")
        else:
            db.session.commit()


class ModelBase(db.Model, BaseMethod):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(db.DateTime, unique=True, nullable=True)
    date_update = db.Column(db.DateTime, nullable=True)
