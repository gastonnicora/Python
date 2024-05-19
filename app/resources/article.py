from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.article import Article
from app.helpers.token import token_required
from app.socket.socketio import emit_finish, emit_start


@token_required
@validate_request("Articulos","articleCreate")
def create(current_user): 
    sms=Article.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Article.all()
    return jsonify(sms.dump()),sms.cod

def get(uuid):
    sms=Article.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Articulos","articleUpdate")
def update(session): 
    sms=Article.update(request.get_json(),session["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    article= Article.get(uuid)    
    sms= Article.delete(uuid,session["uuid"])
    if not sms.dump()["error"]:
        before= article.dump()["content"]["before"]
        next= article.dump()["content"]["next"]
        if before and next:
            Article.setBefore(before,next)
            Article.setNext(next,before)
        elif before:
            Article.setNext(None,before)
        elif next:
            Article.setBefore(None,next)
    return jsonify(sms.dump()),sms.cod

def start(uuid):
    sms= Article.setStarted(uuid)
    emit_start(uuid, sms.dump()["content"]["timeAfterBid"])
    return jsonify(sms.dump()),sms.cod

def finish(uuid):
    sms= Article.setFinished(uuid)
    emit_finish(uuid)
    if  sms.dump()["content"]["tipe"] ==1 and sms.dump()["content"]["next"]:
        sms= Article.setStarted(sms.dump()["content"]["next"])
        emit_start(uuid, sms.dump()["content"]["next"])
    return jsonify(sms.dump()),sms.cod


