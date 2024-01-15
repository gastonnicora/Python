from flask import request, jsonify
import jwt
from functools import wraps
from os import environ
def token_required_celery(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token or token=="null" or token == "undefined":
            return jsonify({'error': 'Por favor inicie sesión para realizar esta acción',"cod":401}),401

        try:
            from app.helpers.celery import Celery
            data = jwt.decode(token, environ.get("SECRET_KEY", "1234"), algorithms="HS256") 
            if (Celery()._getUuid() != data["uuid"]):
                 return jsonify({'error': 'Por favor vuelva a iniciar sesión para realizar esta acción',"cod":401}),401
        except:
            return jsonify({'error': 'Por favor vuelva a iniciar sesión para realizar esta acción',"cod":401}),401

        return f( *args, **kwargs)
    return decorator 