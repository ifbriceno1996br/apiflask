import os
import redis
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

BASE_DIR_P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_API = os.path.join(BASE_DIR_P, 'api')

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
socket = SocketIO()
jwt = JWTManager()
redis = redis.Redis(host='127.0.0.1', port=6379)
