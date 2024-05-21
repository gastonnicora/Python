from flask import jsonify,  request, abort
from app.helpers.token import token_required
from app.models.user import User
from app.helpers.message import Message
from app.models.confirmEmail import ConfirmEMail
from app.helpers.validador import validate_request


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


@token_required 
def delete(uuid):
    sms= ConfirmEMail.get(uuid)
    if sms.cod== 202 :
        ConfirmEMail.delete(uuid)
        User.delete(sms.content.user)
        return jsonify({"content":"Eliminado con éxito"}),202
    else:
        return jsonify({"content":"La confirmación no existe"}),400
