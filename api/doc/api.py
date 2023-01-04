# from flask import Blueprint
# from flask_restx import Api, Resource, fields
#
# bp_api = Blueprint('bp_api', __name__, url_prefix='/api')
#
# api_user = Api(bp_api, version='1.0', title='Api', description="api")
#
# resource_fields = api_user.model('Resource', {
#     'name': fields.String,
# })
#
#
# @api_user.route("/recurso/")
# @api_user.doc(desciption="prueba")
# class Login(Resource):
#
#     @api_user.marshal_with(resource_fields, as_list=True)
#     def get(self, id):
#         return {"id": 1}
#
#     @api_user.doc(responses={403: 'Not Authorized'})
#     def post(self, id):
#         api_user.abort(403)
#
#     def put(self, id):
#         return {}
#
#     def patch(self, id):
#         return {}
