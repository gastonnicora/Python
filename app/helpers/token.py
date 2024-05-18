import os
from flask import request, jsonify, make_response
import jwt
from functools import wraps
from os import environ
from app.helpers.sessions import Sessions
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token or token=="null" or token == "undefined":
            return jsonify({'error': 'Por favor inicie sesión para realizar esta acción',"cod":401}),401

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms="HS256") 
            current_user = Sessions().getSession(data['uuid'])
        except:
            return jsonify({'error': 'Por favor vuelva a iniciar sesión para realizar esta acción',"cod":401}),401

        return f(current_user, *args, **kwargs)
    return decorator