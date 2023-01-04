from flask import Blueprint, request, jsonify, Response
from api.user.models import User
from config.settings import socket
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from functools import wraps

user = Blueprint('user', __name__, url_prefix='/user')



@user.route('/list', methods=['GET'])
def list_users():
    data = {}
    try:
        if request.method == 'GET':
            print("hola desd egt")
            data = []
            users = User.query.all()
            for item in users:
                data.append(item.toJSON())
            socket.emit("message", {'hola': 'prueba'})
    except Exception as e:
        print("Error", str(e))
    return jsonify(data), 200


@user.route('/list/<int:pk>', methods=['GET'])
def list_user(pk):
    data = {}
    try:
        if request.method == 'GET':
            user = User.query.filter_by(id=pk).first()
            if user:
                data = user.toJSON()
            else:
                data = {'error': 'El recurso no existe'}
    except Exception as e:
        print("Error", str(e))
    return jsonify(data), 200


@user.route('/edit/<int:pk>', methods=['PUT'])
def edit_user(pk):
    data = {}
    try:
        if request.method == 'PUT':
            user = User.query.filter_by(id=pk)
            if user.first():
                data = request.json
                user = user.first()
                password = data['password']
                email = data['email']
                first_name = data['first_name']
                last_name = data['last_name']
                user.password = password
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                data = {'message': 'Se actualizo el recurso correctamente'}
            else:
                data = {'error': 'El recurso no esta disponible'}
        else:
            data = {'error': 'metodo no permitido'}
    except Exception as e:
        print("Error", str(e))
    return jsonify(data)


@user.route('/add', methods=['POST'])
def add_user():
    data = {}
    try:
        if request.method == 'POST':
            data = request.json
            username = data['username']
            password = data['password']
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            data = {'message': 'usuario creado'}
        else:
            data = {'error': 'metodo no permitido'}
    except Exception as e:
        print("Error", str(e))
    return jsonify(data)
