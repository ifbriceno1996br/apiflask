from datetime import datetime, timezone, timedelta
from flask import render_template, redirect, url_for, request
from flask_jwt_extended import get_jwt, create_access_token
from config.app import create_app
from config.settings import socket
from socketflask import consumers  # Esta importacion carga los eventos de socket de la aplicacions

app = create_app()


@app.before_request
def before_request():
    print("endpoint", request.endpoint)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/prueba')
def prueba():  # put application's code here
    return "Hola desde prrueba"


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0')
