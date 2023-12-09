from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.company import Company
from app.helpers.token import token_required

@token_required
def create(current_user): 
    v= Validador("Empresas","companyCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Company.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Company.all()
    return jsonify(sms.dump()),sms.cod

def get(uuid):
    sms=Company.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("Empresas","companyUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Company.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Company.delete(uuid)
    return jsonify(sms.dump()),sms.cod