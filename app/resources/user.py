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
    request_data = {
        "method": request.method,
        "url": request.url,
        "base_url": request.base_url,
        "host_url": request.host_url,
        "path": request.path,
        "full_path": request.full_path,
        "headers": {header: value for header, value in request.headers.items()},
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.get_json(silent=True),
        "cookies": request.cookies.to_dict(),
        "remote_addr": request.remote_addr,
        "user_agent": str(request.user_agent)
    }
    
    print("Request Data:")
    for key, value in request_data.items():
        print(f"{key}: {value}")
    sms=User.create(request.get_json())
    if sms.error:
        return jsonify(sms.dump()),sms.cod
    else:
        smsConfirm=ConfirmEMail.create(sms.content.uuid)
        if smsConfirm.error:
            return jsonify(smsConfirm.dump()),smsConfirm.cod
        try:
            link = request.origin
            sendEmail(sms.content.email, smsConfirm.content.uuid,link)
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
        data = jwt.decode(token, environ.get("SECRET_KEY","1234"), algorithms="HS256")
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
            token = jwt.encode({'uuid':uuid}, environ.get("SECRET_KEY","1234"), algorithm="HS256")
 
            return jsonify({"content":session,"token":token}),sms.cod

@token_required
def logout(current_user):
    token = request.headers['x-access-tokens']
    data = jwt.decode(token, environ.get("SECRET_KEY","1234"), algorithms="HS256")
    Sessions().deleteSession(data["uuid"])
    sms=Message(content="Sesión cerrada con éxito")
    return jsonify(sms.dump()),sms.cod
    
@token_required
def get(session,uuid):
    sms= User.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Usuarios","userUpdate")
def update(session): 
    sms=User.update(session["uuid"],request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session):
    sms= User.delete(session["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Usuarios","userUpdatePassword")
def updatePassword(session):
    sms=User.updatePassword(session["uuid"],request.get_json())
    return jsonify(sms.dump()),sms.cod