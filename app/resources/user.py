from flask import jsonify,  request, abort
import jwt
from os import environ
from app.models.users import User
from app.helpers.message import Message
from app.helpers.validador import Validador
from app.models.confirmEmail import ConfirmEMail
from app.helpers.sendEmail import sendEmail
from app.helpers.token import token_required
from app.helpers.sessions import Sessions

def create(): 
    v= Validador("Usuarios","userCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=User.create(request.get_json())
    if sms.error:
        return jsonify(sms.dump()),sms.cod
    else:
        smsConfirm=ConfirmEMail.create(sms.content.uuid)
        if smsConfirm.error:
            return jsonify(smsConfirm.dump()),smsConfirm.cod
        sendEmail(sms.content.email, smsConfirm.content.uuid)
       
        return jsonify(sms.dump()),sms.cod

@token_required
def index(session):
    print(session)
    sms = User.all()
    return jsonify(sms.dump()),sms.cod

def login():
    v= Validador("Usuarios","login",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=User.login(request.get_json())
    if sms.error:
        return jsonify(sms.dump()),sms.cod
    else:
        uuid, session= Sessions().addSession(sms.dump()["content"])
        token = jwt.encode({'uuid':uuid}, environ.get("SECRET_KEY", "1234"), algorithm="HS256")
        return jsonify({"content":session,"token":token}),sms.cod
    
@token_required
def get(uuid):
    sms= User.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("Usuarios","userUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=User.update(request.get_json())
    aux=User.get(request.get_json().get("uuid")).content
    if sms.error:
        return jsonify(sms.dump()),sms.cod
    else:
        if sms.content.confirmEmail == 0:
            smsConfirm=ConfirmEMail.create(sms.content.uuid)
            if smsConfirm.error:
                User.update(aux)
                return jsonify(smsConfirm.dump()),smsConfirm.cod
            sendEmail(sms.content.email, smsConfirm.content.uuid)
        return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= User.delete(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def updatePassword(session):
    v= Validador("Usuarios","userUpdatePassword",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=User.updatePassword(request.get_json())
    return jsonify(sms.dump()),sms.cod