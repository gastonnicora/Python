from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.role import Role
from app.helpers.token import token_required

@token_required
def create(current_user): 
    v= Validador("Roles","roleCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Role.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required
def index(session):
    sms = Role.all()
    return jsonify(sms.dump()),sms.cod

@token_required
def get(session,uuid):
    sms=Role.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("Roles","roleUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Role.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Role.delete(uuid)
    return jsonify(sms.dump()),sms.cod