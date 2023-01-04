from flask import Blueprint, request, jsonify

categorias = Blueprint('categorias', __name__, url_prefix='/categorias')


@categorias.route("/list", methods=['POST', 'GET'])
def lista():
    try:
        print("gola")
    except Exception as e:
        print("Error", str(e))
    return jsonify({'hola': "holaaa"})
