from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.company import Company
from app.helpers.token import token_required

@token_required
@validate_request("Empresas","companyCreate")
def create(current_user): 
    sms=Company.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Company.all()
    return jsonify(sms.dump()),sms.cod


def get(uuid):
    sms=Company.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Empresas","companyUpdate")
def update(session): 
    sms=Company.update(request.get_json(),session["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Company.delete(uuid,session["uuid"])
    return jsonify(sms.dump()),sms.cod