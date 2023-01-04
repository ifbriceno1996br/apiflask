# from flask_sqlalchemy import Model
# import sqlalchemy as sa
# from sqlalchemy import MetaData
# from sqlalchemy.ext.declarative import declared_attr
# from sqlalchemy.testing.schema import Table
#
#
# class IdModel(Model):
#     @declared_attr
#     def id(cls):
#         print(cls.__mro__[1:-1])
#         for base in cls.__mro__[1:-1]:
#             if getattr(base, '__table__', None) is not None:
#                 type = sa.ForeignKey(base.id)
#                 break
#         else:
#             type = sa.Integer
#         return sa.Column(type, primary_key=True)
