from functools import wraps
from flask import g, request, redirect, url_for, jsonify


def check_json(f):
    @wraps(f)
    def is_json(*args, **kwargs):
        print("is json", request.is_json)
        if not request.is_json:
            return jsonify({'error': 'formato no valido'})
        return f(*args, **kwargs)
    return is_json
