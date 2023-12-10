from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.permission import Permission
from app.helpers.token import token_required

@token_required
def create(current_user): 
    v= Validador("Permisos","permissionCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Permission.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required
def index(session):
    sms = Permission.all()
    return jsonify(sms.dump()),sms.cod

@token_required
def get(session,uuid):
    sms=Permission.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("Permisos","permissionUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Permission.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Permission.delete(uuid)
    return jsonify(sms.dump()),sms.cod