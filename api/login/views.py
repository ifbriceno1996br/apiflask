import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, current_user, get_jwt, \
    create_refresh_token, get_jti, get_jwt_header, decode_token, verify_jwt_in_request
from api.login.models import TokenBlocklist
from api.user.models import User
from config.settings import jwt, db, socket, redis

auth = Blueprint("login", __name__)


def get_data_redis_login(clave, username):
    data = json.loads(redis.get(clave))
    print("data2",data)
    if isinstance(data,dict):
        print("Existe data")
        data.update({username: {'estado': 'disponible'}})
        redis.set(clave, json.dumps(data))
    data = json.loads(redis.get(clave))
    return data


# Identificamos el usuario que inicio sesion
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Valida que el usaurio cargado exista y lo retorna
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# Validamos que no haya un token bloqueado
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti, status=False).scalar()
    return token is not None


@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload: dict):
    jwtkn = jwt_payload['jti']
    return jsonify({
        'msg': 'token {} already been revoked!'.format(jwtkn)
    }), 401


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload: dict):
    payload = jwt_payload
    user_id = payload['sub']
    token = TokenBlocklist.query.filter_by(user_id=user_id)
    if token.first():
        token.update({'status_refresh': False, 'status': False})
        db.session.commit()
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The token has expired'
    }), 401


@auth.route("/me", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    data = json.loads(redis.get('auditoria_usuarios'))
    return jsonify(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
    )


@auth.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username, password=password).first()
    # Consulta la base de datos por el nombre de usuario y la contraseña
    if user is None:
        return jsonify({'message': 'Bad username or password'}), 401
    else:
        token_login = TokenBlocklist.query.filter_by(user_id=user.id, status=True).first()
        if token_login:
            return jsonify({'message': 'El usuario ya inicio sesion'})
    additional_claims = {"aud": "some_audience", "foo": "bar"}
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    info = decode_token(access_token)
    info_refres = decode_token(refresh_token)
    token = TokenBlocklist(token=access_token, jti=info.get('jti'),
                           user_id=user.id, refresh_token=refresh_token, jti_refresh=info_refres.get("jti"))
    db.session.add(token)
    db.session.commit()
    socket.emit('conexiones', get_data_redis_login('auditoria_usuarios', user.username))

    return jsonify({"access_token": access_token, "refresh_token": refresh_token, "user_id": user.id})


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    token_refresh = request.headers.get("Authorization", None)
    if token_refresh:
        if token_refresh.startswith("Bearer "):
            token = token_refresh.split(" ")[1]
            token_refresh = token
            refresh_token = decode_token(token_refresh)
            token = TokenBlocklist.query.filter_by(jti_refresh=refresh_token.get("jti"), status_refresh=False)
            if token.first():
                return jsonify(error="El token refresh ya no esta disponible, debes iniciar sesion otra vez")
        else:
            return jsonify(error="Bearer no esta en en authorization formato: Bearer token")
    else:
        return jsonify(error="Authorization no esta en header")
    user = User.query.filter_by(id=int(identity)).first()
    if user:
        token = TokenBlocklist.query.filter_by(user_id=identity, status=True)
        if token.first():
            token.update({"status": False})
            db.session.commit()
        access_token = create_access_token(identity=user)
        refresh_token = decode_token(token_refresh)
        jti = decode_token(access_token).get('jti')
        jti_refresh = refresh_token.get("jti")
        new_token = TokenBlocklist(user_id=identity, token=access_token, jti=jti, refresh_token=token_refresh,
                                   jti_refresh=jti_refresh)
        new_token.save()
        return jsonify(access_token=access_token)
    else:
        return jsonify({"error": "user id no existe"})


@auth.route("/current_user", methods=["GET"])
@jwt_required()
def protected_current():
    claims = get_jwt()
    return jsonify({"hola": 'kjsjd'})


@auth.route("/logout", methods=["DELETE"])
@jwt_required()
def modify_token():
    token = get_jwt()
    jti = token['jti']
    id_user = token['sub']
    user = TokenBlocklist.query.filter_by(user_id=id_user, status=True)
    if user.first():
        username = User.query.get(id_user).username
        user.update({'status': False, 'status_refresh': False})
        db.session.commit()
        data = json.loads(redis.get('auditoria_usuarios'))
        if data.get(username):
            data.pop(username)
            print("data", data)
            redis.set("auditoria_usuarios", json.dumps(data))
            socket.emit("conexiones", data)
    else:
        return jsonify(error="El usuario en jwt no existe")
    return jsonify(msg="JWT revoked")
