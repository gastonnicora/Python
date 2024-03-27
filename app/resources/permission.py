from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.permission import Permission
from app.helpers.token import token_required

@token_required
@validate_request("Permisos","permissionCreate")
def create(current_user): 
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
@validate_request("Permisos","permissionUpdate")
def update(session): 
    sms=Permission.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Permission.delete(uuid)
    return jsonify(sms.dump()),sms.cod