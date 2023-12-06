from flask import jsonify,  request, abort
from app.models.users import User
from app.helpers.message import Message
from app.helpers.validador import Validador
from app.models.confirmEmail import ConfirmEMail
from app.helpers.sendEmail import sendEmail

def create(): 
    v= Validador("Usuarios","createUser",request.get_json())
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

def index():
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
        
        return jsonify(sms.dump()),sms.cod