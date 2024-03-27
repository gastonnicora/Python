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
def get(session,uuid):
    sms=Employee.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def getByUser(session,uuid):
    sms=Employee.getByUser(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def getByCompany(session,uuid):
    sms=Employee.getByCompany(uuid)
    return jsonify(sms.dump()),sms.cod



@token_required 
def delete(session,uuid):
    sms= Employee.delete(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required 
def deleteByUser(session,uuid):
    sms= Employee.deleteByUser(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required 
def deleteByCompany(session,uuid):
    sms= Employee.deleteByCompany(uuid)
    return jsonify(sms.dump()),sms.cod