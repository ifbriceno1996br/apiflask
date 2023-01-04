from engineio import json
from flask_socketio import emit
from config.settings import socket, redis

usuarios = {}


@socket.on("connect")
def connect():
    print("socket conectado")


@socket.on("disconnect")
def connect():
    socket.stop()


@socket.on("message")
def message(mensaje):
    emit("message", {'hola': 'hola'})


@socket.on("conexiones")
def logueo(mensaje):
    if mensaje['conexion'] == 1:
        data = json.loads(redis.get('auditoria_usuarios'))
        emit("conexiones", data, broadcast=True)
