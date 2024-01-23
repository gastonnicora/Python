from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.article import Article
from app.helpers.token import token_required
from app.helpers.tokenCelery import token_required_celery

@token_required
def create(current_user): 
    v= Validador("Articulos","articleCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Article.create(request.get_json())
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Article.all()
    return jsonify(sms.dump()),sms.cod

def get(uuid):
    sms=Article.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("Articulos","articleUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Article.update(request.get_json())
    return jsonify(sms.dump()),sms.cod

@token_required 
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
    return Article.setStarted(uuid)

@token_required_celery
def finish(uuid):
    return Article.setFinished(uuid)
