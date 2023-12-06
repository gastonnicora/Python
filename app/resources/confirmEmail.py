from flask import jsonify,  request, abort
from app.models.users import User
from app.helpers.message import Message
from app.models.confirmEmail import ConfirmEMail

def confirm(uuid): 
    sms=ConfirmEMail.get(uuid)
    if(sms.error):
        return jsonify(sms.dump()),sms.cod
    smsConfirmDelete= ConfirmEMail.delete(uuid)
    smsUser=User.confirm(sms.content.user)
    if(smsConfirmDelete.error):
        return jsonify(smsConfirmDelete.dump()),smsConfirmDelete.cod
    return jsonify(smsUser.dump()),smsUser.cod

def index():
    sms = ConfirmEMail.all()
    return jsonify(sms.dump()),sms.cod

def get(uuid):
    sms= ConfirmEMail.get(uuid)
    return jsonify(sms.dump()),sms.cod
