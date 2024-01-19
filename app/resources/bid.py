from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.bid import Bid
from app.helpers.token import token_required

@token_required
def create(current_user): 
    v= Validador("Empresas","companyCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Bid.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Bid.all()
    return jsonify(sms.dump()),sms.cod

def get(uuid):
    sms=Bid.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("Empresas","companyUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Bid.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Bid.delete(uuid)
    return jsonify(sms.dump()),sms.cod