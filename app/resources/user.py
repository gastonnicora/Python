from flask import jsonify,  request, abort
import jwt
from os import environ
from app.models.user import User
from app.helpers.message import Message
from app.helpers.validador import validate_request, Validador
from app.models.confirmEmail import ConfirmEMail
from app.helpers.sendEmail import sendEmail
from app.helpers.token import token_required
from app.helpers.sessions import Sessions

@validate_request("Usuarios","userCreate")
def create(): 
    sms=User.create(request.get_json())
    if sms.error:
        return jsonify(sms.dump()),sms.cod
    else:
        smsConfirm=ConfirmEMail.create(sms.content.uuid)
        if smsConfirm.error:
            return jsonify(smsConfirm.dump()),smsConfirm.cod
        try:
            sendEmail(sms.content.email, smsConfirm.content.uuid)
        except:
          print('An exception occurred')
        from app.helpers.celery import deleteConfirm
        deleteConfirm(smsConfirm.content.uuid)
       
        return jsonify(sms.dump()),sms.cod

@token_required
def index(session):
    sms = User.all()
    return jsonify(sms.dump()),sms.cod


def login():
    token = request.headers['x-access-tokens']
    current_user=None
    try:
        data = jwt.decode(token, environ.get("SECRET_KEY", "1234"), algorithms="HS256")
        current_user = Sessions().getSession(data['uuid'])
    finally:
        if current_user:
            return jsonify({"error":"Usted ya inicio sesión. Cierre sesión si quiere iniciar una nueva ","cod":400}),400
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
def logout(current_user):
    token = request.headers['x-access-tokens']
    data = jwt.decode(token, environ.get("SECRET_KEY", "1234"), algorithms="HS256")
    Sessions().deleteSession(data["uuid"])
    sms=Message(content="Sesión cerrada con éxito")
    return jsonify(sms.dump()),sms.cod
    
@token_required
@validate_request("Usuarios","user")
def get(session,uuid):
    sms= User.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Usuarios","userUpdate")
def update(session): 
    sms=User.update(session["uuid"],request.get_json())
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
@validate_request("Usuarios","userDelete")
def delete(session,uuid):
    sms= User.delete(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Usuarios","userUpdatePassword")
def updatePassword(session):
    sms=User.updatePassword(request.get_json())
    return jsonify(sms.dump()),sms.cod