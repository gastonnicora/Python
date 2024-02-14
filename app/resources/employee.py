from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.employee import Employee
from app.helpers.token import token_required

@token_required
@validate_request("Empleados","employeeCreate")
def create(session): 
    sms=Employee.create(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required
def index(session):
    sms = Employee.all()
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Empleados","employee")
def get(session,uuid):
    sms=Employee.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Empleados","employeeByUser")
def getByUser(session,uuid):
    sms=Employee.getByUser(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Empleados","employeeByCompany")
def getByCompany(session,uuid):
    sms=Employee.getByCompany(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Empleados","employeeUpdate")
def update(session): 
    sms=Employee.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
@validate_request("Empleados","employeeDelete")
def delete(session,uuid):
    sms= Employee.delete(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required 
@validate_request("Empleados","employeeDeleteByUser")
def deleteByUser(session,uuid):
    sms= Employee.deleteByUser(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required 
@validate_request("Empleados","employeeDeleteByCompany")
def deleteByCompany(session,uuid):
    sms= Employee.deleteByCompany(uuid)
    return jsonify(sms.dump()),sms.cod