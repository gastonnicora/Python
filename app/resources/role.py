from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.role import Role
from app.helpers.token import token_required

@token_required
@validate_request("Roles","roleCreate")
def create(current_user): 
    sms=Role.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required
def index(session):
    sms = Role.all()
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Roles","role")
def get(session,uuid):
    sms=Role.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Roles","roleUpdate")
def update(session): 
    sms=Role.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
@validate_request("Roles","roleDelete")
def delete(session,uuid):
    sms= Role.delete(uuid)
    return jsonify(sms.dump()),sms.cod