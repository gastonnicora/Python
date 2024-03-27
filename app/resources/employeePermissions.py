from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.employeePermissions import EmployeePermissions
from app.helpers.token import token_required

@token_required
@validate_request("PermisosDeEmpleado","employeePermissionsCreate")
def create(current_user): 
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
def delete(session,uuid):
    sms= EmployeePermissions.delete(uuid)
    return jsonify(sms.dump()),sms.cod