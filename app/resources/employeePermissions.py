from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.employeePermissions import EmployeePermissions
from app.helpers.token import token_required

@token_required
def create(current_user): 
    v= Validador("PermisosDeEmpleado","employeePermissionsCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=EmployeePermissions.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required
def index(session):
    sms = EmployeePermissions.all()
    return jsonify(sms.dump()),sms.cod

@token_required
def get(session,uuid):
    sms=EmployeePermissions.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("PermisosDeEmpleado","employeePermissionsUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=EmployeePermissions.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= EmployeePermissions.delete(uuid)
    return jsonify(sms.dump()),sms.cod