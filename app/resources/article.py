from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.article import Article
from app.helpers.token import token_required
from app.helpers.tokenCelery import token_required_celery
from app.socket.socketio import emit_finish, emit_start


@token_required
@validate_request("Articulos","articleCreate")
def create(current_user): 
    sms=Article.create(request.get_json())
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Article.all()
    return jsonify(sms.dump()),sms.cod

@validate_request("Articulos","article")
def get(uuid):
    sms=Article.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Articulos","articleUpdate")
def update(session): 
    sms=Article.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
@validate_request("Articulos","articleDelete")
def delete(session,uuid):
    article= Article.get(uuid)
    sms= Article.delete(uuid)
    before= article.before
    next= article.next
    if before and next:
        Article.setBefore(before,next)
        Article.setNext(next,before)
    elif before:
        Article.setNext(None,before)
    elif next:
        Article.setBefore(None,next)
    return jsonify(sms.dump()),sms.cod

@token_required_celery
def start(uuid):
    sms= Article.setStarted(uuid)
    emit_start(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required_celery
def finish(uuid):
    sms= Article.setFinished(uuid)
    emit_finish(uuid)
    return jsonify(sms.dump()),sms.cod


